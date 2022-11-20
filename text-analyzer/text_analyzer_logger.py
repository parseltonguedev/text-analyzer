import logging

TIME_FORMAT = "%I:%M:%S%p on %B %d, %Y"
LOG_FORMAT = (
    "[%(asctime)s] [%(text_source)s] [%(source_name)s] [%(levelname)s] - %(message)s"
)
WEB_RESOURCE = "web resource"
LOCAL_FILE = "local file"


class SourceNotSupported(Exception):
    pass


logger = logging.getLogger("text_analyzer")
formatter = logging.Formatter(LOG_FORMAT)

stdout_handler = logging.StreamHandler()
file_handler = logging.FileHandler("../text_analyzer.log", encoding="utf-8")

logger.setLevel(logging.DEBUG)
stdout_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

stdout_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(stdout_handler)
logger.addHandler(file_handler)
