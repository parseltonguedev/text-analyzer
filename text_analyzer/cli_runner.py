import concurrent.futures
import logging
import time

import click

from text_analyzer_runner import text_analyzer_runner


@click.command()
@click.argument("file_names", nargs=-1)
@click.option('--view', default=None, help='get text report from database (if exist)')
def main(file_names, view):
    """
    Text analyzer runs from the console, and you can specify a file name(s), resource(s).
    The "Text analyzer" is capable of processing multiple files/resources at the same time.\n
    Example with local text files: python main.py file1.txt file2.txt file3.txt
    Example with web resources: python main.py https://www.cl.cam.ac.uk/~mgk25/ucs/examples/UTF-8-demo.txt
    """
    start_total_time = time.perf_counter()
    logger = logging.getLogger("text_analyzer")

    with concurrent.futures.ProcessPoolExecutor() as pool:
        pool.map(text_analyzer_runner, file_names)

    total_execution_time = (time.perf_counter() - start_total_time) * 1000
    logger.info(
        f"The time taken to process all texts: {total_execution_time:.2f} ms",
        extra={"text_source": "provided sources", "source_name": file_names},
    )


if __name__ == "__main__":
    main()
