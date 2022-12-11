import logging
import os

import requests
import validators
from nltk.corpus import PlaintextCorpusReader, stopwords
from nltk.tokenize import sent_tokenize

from text_analyzer_logger import LOCAL_FILE, WEB_RESOURCE, SourceNotSupported


class Text:
    current_folder = os.getcwd()
    text_files_folder_name = os.path.join(current_folder, "text_files")
    reversed_texts_folder_name = os.path.join(current_folder, "reversed")
    reversed_intact_folder_name = os.path.join(current_folder, "reversed_intact")
    texts_analysis_folder_name = os.path.join(current_folder, "texts_analysis")
    os.makedirs(text_files_folder_name, exist_ok=True)
    os.makedirs(reversed_texts_folder_name, exist_ok=True)
    os.makedirs(reversed_intact_folder_name, exist_ok=True)
    os.makedirs(texts_analysis_folder_name, exist_ok=True)
    stop_words = set(stopwords.words("english"))

    logger = logging.getLogger("text_analyzer")

    def __init__(self, file_name: str):
        if not file_name.endswith(".txt") or validators.url(file_name):
            self.logger.error(
                "Text analyzer doesn't support provided source. "
                "Provide web resource with text or local text file name",
                extra={
                    "text_source": WEB_RESOURCE
                    if validators.url(file_name)
                    else LOCAL_FILE,
                    "source_name": self.file_name,
                },
            )
            raise SourceNotSupported(
                "Text analyzer doesn't support provided source. Provide web resource with text or local text file name"
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
                text = PlaintextCorpusReader(
                    self.text_files_folder_name, self.file_name
                )
            except FileNotFoundError as file_not_found_exception:
                self.logger.error(
                    f"File not found in {self.text_files_folder_name} with {file_not_found_exception}",
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
            self.logger.error(
                f"Unexpected requests exception {requests_exception}",
                extra={"text_source": self.source, "source_name": self.file_name},
            )

        with open(downloaded_file_name, "w", encoding="utf-8") as download:
            self.file_name = downloaded_file_name
            download.write(content.text)

        return PlaintextCorpusReader(self.text_files_folder_name, downloaded_file_name)
