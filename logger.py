import logging

logging.basicConfig(
    level=logging.INFO,
    filename="E:/ESL/download.log",
    format='%(asctime)s - %(name)s - %(filename)s[line:%(lineno)d] %(levelname)s msg: %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filemode="w"
)

logger = logging.getLogger("esl_download")

