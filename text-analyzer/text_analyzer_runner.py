import logging
import time
from datetime import datetime

import validators

from text_analyzer import TextAnalyzer
from text_analyzer_logger import LOCAL_FILE, TIME_FORMAT, WEB_RESOURCE
from text_parser import Text


def text_analyzer_runner(text_file_name: str):
    logger = logging.getLogger("text_analyzer")
    start_time = time.time()
    start_date_time_string = datetime.now().strftime(TIME_FORMAT)
    try:
        text = Text(text_file_name)
    except Exception as exception:
        logger.error(
            f"Unexpected error occurred {exception}",
            extra={
                "text_source": WEB_RESOURCE
                if validators.url(text_file_name)
                else LOCAL_FILE,
                "source_name": text_file_name,
            },
        )
    else:
        logger.info(
            f"Report generation for {text_file_name} started at: {start_date_time_string}",
            extra={
                "text_source": WEB_RESOURCE
                if validators.url(text_file_name)
                else LOCAL_FILE,
                "source_name": text_file_name,
            },
        )
        text_analyzer = TextAnalyzer(text)
        analysis_result = text_analyzer.get_text_analysis()
        execution_time = (time.time() - start_time) * 1000
        logger.info(
            f"The time taken to process the {text_file_name} text {execution_time:.2f} ms",
            extra={
                "text_source": WEB_RESOURCE
                if validators.url(text_file_name)
                else LOCAL_FILE,
                "source_name": text_file_name,
            },
        )
        return analysis_result
