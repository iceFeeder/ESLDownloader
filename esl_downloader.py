
from HTMLParser import HTMLParser
from logger import logger
from gevent import monkey
monkey.patch_all()
import requests
import gevent
import re
import os

esl_url = "https://www.eslpod.com/website/show_all.php?cat_id=-59456&low_rec=%s"
download_path = "E:/ESL"
index = 0

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            _ , link = attrs[0]
            if "mp3" in link:
                self.links.append(link)

parser = MyHTMLParser()
replace_reg = re.compile(r"<! (.*) >")

def download(url,path=download_path):
    count = 0
    file_name = os.path.basename(url)
    src_path = path+'/'+file_name
    while True:
        try:
            res = requests.get(url, stream=True)
            if res.status_code == 200:
                with open(src_path,"wb") as f:
                    logger.info("Starting download %s to %s" % (url,src_path))
                    for chunk in res.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                    f.close()
                    logger.info("Finished download %s." % url)
                    break
        except Exception ,e:
            logger.error("Exception msg: %s" % str(e))
        logger.error("Failed to download %s. Try again..." % url)
        count += 1
        if count > 5:
            logger.error("Failed to download %s 5 times. No more try..." % url)
            break

while True:
    parser.links = []
    res = requests.get(esl_url % index)
    content = replace_reg.sub("",res.content)
    parser.feed(content)
    if res.status_code != 200:
        logger.error("status_code: %s" % res.status_code)
        continue
    else:
        logger.info("links: %s" % parser.links.__str__())
        if parser.links == [] :
            logger.info("Finished all tasks.")
            break
        gevent.joinall(
            [
                gevent.spawn(download,url) for url in parser.links
            ]
        )
    index += 20

