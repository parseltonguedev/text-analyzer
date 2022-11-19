import json
import logging
import multiprocessing
import os
import re
import time
from datetime import datetime

import click
import requests
import validators
from nltk import FreqDist
from nltk.corpus import PlaintextCorpusReader, stopwords
from nltk.tokenize import sent_tokenize

TIME_FORMAT = "%I:%M:%S%p on %B %d, %Y"
LOG_FORMAT = "[%(asctime)s] [%(text_source)s] [%(source_name)s] [%(levelname)s] - %(message)s"
WEB_RESOURCE = "web resource"
LOCAL_FILE = "local file"

logger = logging.getLogger("text_analyzer")
formatter = logging.Formatter(LOG_FORMAT)

stdout_handler = logging.StreamHandler()
file_handler = logging.FileHandler("../text_analyzer.log", encoding="utf-8")

logger.setLevel(logging.INFO)
stdout_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)

stdout_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(stdout_handler)
logger.addHandler(file_handler)


class SourceNotSupported(Exception):
    pass


class Text:
    current_folder = os.getcwd()
    stop_words = set(stopwords.words("english"))

    def __init__(self, file_name: str):
        if not file_name.endswith(".txt") or (
            not file_name.endswith(".txt") and not file_name.startswith("http")
        ):
            raise SourceNotSupported(
                f"Text analyzer doesn't support provided source. Provide web resource with text or local text file name"
            )

        self.file_name = file_name
        self.source = LOCAL_FILE
        self.file_corpus_reader = self.get_text()
        self.raw = self.file_corpus_reader.raw()
        self.paragraphs = self.file_corpus_reader.paras()
        self.sentences = sorted(self.file_corpus_reader.sents(), key=len, reverse=True)
        self.tokenized_sentences = sent_tokenize(self.raw)
        self.words = sorted(
            [
                word.lower()
                for word in self.file_corpus_reader.words()
                if word.isalpha()
                and word.lower() not in self.stop_words
                and len(word) > 1
            ],
            key=len,
            reverse=True,
        )
        self.characters = [character for word in self.words for character in word]

    def get_text(self) -> PlaintextCorpusReader:
        if validators.url(self.file_name):
            text = self.get_file_from_web_resource(self.file_name)
            return text
        elif self.file_name.endswith(".txt"):
            try:
                text = PlaintextCorpusReader(self.current_folder, self.file_name)
            except FileNotFoundError as file_not_found_exception:
                logger.error(
                    f"File not found in {self.current_folder} with {file_not_found_exception}",
                    extra={"text_source": self.source, "source_name": self.file_name},
                )
            else:
                return text

    def get_file_from_web_resource(self, resource_url: str) -> PlaintextCorpusReader:
        self.source = "web resource"
        downloaded_file_name = resource_url.split("/")[-1]

        try:
            with requests.Session() as session:
                content = session.get(resource_url)
        except requests.exceptions.RequestException as requests_exception:
            logger.error(
                f"Unexpected requests exception {requests_exception}",
                extra={"text_source": self.source, "source_name": self.file_name},
            )

        with open(downloaded_file_name, "w", encoding="utf-8") as download:
            self.file_name = downloaded_file_name
            download.write(content.text)

        return PlaintextCorpusReader(self.current_folder, downloaded_file_name)


class TextAnalyzer:
    def __init__(self, text: Text):
        self.text = text

    def get_text_analysis(self):
        analysis_results = {
            "The number of paragraphs": self.get_number_of_paragraphs(),
            "The number of sentences": self.get_number_of_sentences(),
            "The number of words": self.get_number_of_words(),
            "The number of characters": self.get_number_of_characters(),
            "Frequency of characters": self.get_characters_frequency(),
            "Distribution of characters": self.get_characters_distribution(),
            "The average word length": self.get_average_word_length(),
            "The average number of words in a sentence": self.get_average_number_of_words_in_a_sentence(),
            "Top 10 most used words": self.get_n_most_used_words(10),
            "Top 10 longest words": self.get_n_longest_words(10),
            "Top 10 shortest words": self.get_n_shortest_words(10),
            "Top 10 longest sentences": self.get_n_longest_sentences(10),
            "Top 10 shortest sentences": self.get_n_shortest_sentences(10),
            "The number of palindrome words": self.get_number_of_palindromes(),
            "Top 10 longest palindrome words": self.get_n_palindrome_words(10),
            "Is the whole text a palindrome": self.is_text_a_palindrome(),
            "Is the all words in text palindromes": self.is_all_words_palindromes(),
            "Reversed text saved to": self.get_reversed_text(self.text.file_name),
            "Reversed text with the characters order in the words kept intact saved to":
                self.get_reversed_text_with_characters_in_words_intact(self.text.file_name),
            f"Report generated for {self.text.file_name} at (date and time)":
                datetime.now().strftime(TIME_FORMAT),
        }

        for topic, result in analysis_results.items():
            logger.info(
                f"{topic.upper()}: {result}",
                extra={
                    "text_source": self.text.source,
                    "source_name": self.text.file_name,
                },
            )

        analysis_file_name = (
            f"analysis_results_{self.text.file_name.replace('.txt', '.json')}"
        )

        with open(analysis_file_name, "w", encoding="utf-8") as analysis_results_file:
            json.dump(
                analysis_results, analysis_results_file, indent=4, ensure_ascii=False
            )

        return analysis_results

    def get_number_of_characters(self) -> int:
        return len(self.text.characters)

    def get_number_of_paragraphs(self) -> int:
        return len(self.text.paragraphs)

    def get_number_of_words(self) -> int:
        return len(self.text.words)

    def get_number_of_sentences(self) -> int:
        return len(self.text.sentences)

    def get_characters_frequency(self):
        characters_frequency = dict(FreqDist(self.text.characters).most_common())
        return characters_frequency

    def get_characters_distribution(self):
        if not self.text.characters:
            return {}

        characters_distribution = {
            character: round(frequency * 100 / len(self.text.characters), 3)
            for character, frequency in self.get_characters_frequency().items()
        }
        return characters_distribution

    def get_average_word_length(self):
        if not self.text.words:
            return 0

        return round(
            sum((len(word) for word in self.text.words)) / len(self.text.words)
        )

    def get_average_number_of_words_in_a_sentence(self):
        if not self.text.sentences:
            return 0

        return round(
            sum((len(sentence) for sentence in self.text.sentences))
            / len(self.text.sentences)
        )

    def get_n_most_used_words(self, number_of_words: int):
        return dict(self.get_words_frequency()[:number_of_words])

    def get_n_longest_words(self, number_of_words: int):
        longest_words = sorted(set(self.text.words), key=len, reverse=True)[
            :number_of_words
        ]
        return longest_words

    def get_n_shortest_words(self, number_of_words: int):
        shortest_words = sorted(set(self.text.words), key=len, reverse=True)[
            : -number_of_words - 1: -1
        ]
        return shortest_words

    def _get_unique_sentences(self):
        unique_sentences = sorted(
            [
                list(unique_sentence)
                for unique_sentence in set(
                    [tuple(sentence) for sentence in self.text.sentences]
                )
            ],
            key=len,
            reverse=True,
        )
        return unique_sentences

    def _get_sentences_sorted_by_length(self):
        return sorted(self.text.tokenized_sentences, key=len, reverse=True)

    def get_n_longest_sentences(self, number_of_sentences):
        sentences_by_length = self._get_sentences_sorted_by_length()
        return sentences_by_length[:number_of_sentences]

    def get_n_shortest_sentences(self, number_of_sentences):
        sentences_by_length = self._get_sentences_sorted_by_length()
        return sentences_by_length[: -number_of_sentences - 1: -1]

    def get_number_of_palindromes(self):
        return len(self.get_palindrome_words())

    def get_n_palindrome_words(self, number_of_words):
        palindrome_words = self.get_palindrome_words()
        return palindrome_words[:number_of_words] if palindrome_words else []

    def get_words_frequency(self):
        words_frequency = FreqDist(self.text.words).most_common()
        return words_frequency

    def get_palindrome_words(self):
        palindrome_words = sorted(
            set(
                [
                    word
                    for word in self.text.words
                    if str(word).lower() == str(word).lower()[::-1]
                ]
            ),
            key=len,
            reverse=True,
        )
        return palindrome_words

    def is_text_a_palindrome(self):
        filtered_text = "".join(
            letter.lower() for letter in self.text.raw if letter.isalnum()
        )
        return filtered_text == filtered_text[::-1]

    def is_all_words_palindromes(self):
        return sorted(self.text.words) == sorted(self.get_palindrome_words())

    def get_reversed_text(self, file_name):
        reversed_text = self.text.raw[::-1]
        reversed_text_file_name = f"reversed_{file_name}"

        with open(reversed_text_file_name, "w", encoding="utf-8") as reversed_text_file:
            reversed_text_file.write(reversed_text)

        return reversed_text_file_name

    def get_reversed_text_with_characters_in_words_intact(self, file_name):
        revered_sentences_with_words_intact = []

        for sentence in self.text.file_corpus_reader.sents():
            sub_formatted_sentences = re.sub(
                r""" ([.,:'"!?\[\]\-])""", r"\g<1>", " ".join(sentence[::-1])
            )
            formatted_sentences = re.sub(
                r"""([.';:"!\[\]\-]) """,
                r"\g<1>",
                " ".join(sub_formatted_sentences.split()),
            )
            revered_sentences_with_words_intact.append(formatted_sentences)

        reversed_text_intact = " ".join(revered_sentences_with_words_intact)
        reversed_text_words_intact_file_name = f"reversed_words_intact_{file_name}"

        with open(
            reversed_text_words_intact_file_name, "w", encoding="utf-8"
        ) as reversed_text_words_intact_file:
            reversed_text_words_intact_file.write(reversed_text_intact)

        return reversed_text_words_intact_file_name


def text_analyzer_runner(text_file_name: str):
    start_time = time.time()
    start_date_time_string = datetime.now().strftime(TIME_FORMAT)
    logger.info(
        f"Report generation for {text_file_name} started at: {start_date_time_string}",
        extra={
            "text_source": WEB_RESOURCE
            if validators.url(text_file_name)
            else LOCAL_FILE,
            "source_name": text_file_name,
        },
    )
    text = Text(text_file_name)
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


@click.command()
@click.argument("file_names", nargs=-1)
def main(file_names):
    """
    Text analyzer runs from the console, and you can specify a file name(s), resource(s).
    The "Text analyzer" is capable of processing multiple files/resources at the same time.\n
    Example with local text files: python main.py file1.txt file2.txt file3.txt
    Example with web resources: python main.py https://www.cl.cam.ac.uk/~mgk25/ucs/examples/UTF-8-demo.txt

    """
    start_total_time = time.time()

    with multiprocessing.Pool() as pool:
        pool.map(text_analyzer_runner, file_names)

    total_execution_time = (time.time() - start_total_time) * 1000
    logger.info(
        f"The time taken to process all texts: {total_execution_time:.2f} ms",
        extra={"text_source": "provided sources", "source_name": file_names},
    )


if __name__ == "__main__":
    main()
