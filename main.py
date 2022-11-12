import json
import multiprocessing
import os
import time
from datetime import datetime
from urllib.request import urlopen

from nltk import FreqDist
from nltk.corpus import PlaintextCorpusReader, stopwords


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
        self.file_corpus_reader = self.get_text(file_name)
        self.raw = self.file_corpus_reader.raw()
        self.paragraphs = self.file_corpus_reader.paras()
        self.sentences = sorted(self.file_corpus_reader.sents(), key=len, reverse=True)
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

    def get_text(self, file_name: str) -> PlaintextCorpusReader:
        if file_name.startswith("http") and file_name.endswith(".txt"):
            text = self.get_file_from_web_resource(file_name)
            return text
        elif file_name.endswith(".txt"):
            text = PlaintextCorpusReader(self.current_folder, file_name)
            return text

    def get_file_from_web_resource(self, resource_url: str) -> PlaintextCorpusReader:
        downloaded_file_name = resource_url.split("/")[-1]

        with urlopen(resource_url) as webpage:
            content = webpage.read()

        with open(downloaded_file_name, "wb") as download:
            self.file_name = downloaded_file_name
            download.write(content)

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
            "Is the whole text a palindrome": self.is_text_palindrome(),
            "Reversed text": self.get_reversed_text(self.text.file_name),
            "Reversed text with the characters order in the words kept intact":
                self.get_reversed_text_with_characters_in_words_intact(self.text.file_name),
        }

        analysis_file_name = (
            f"analysis_results_{self.text.file_name.replace('.txt', '.json')}"
        )

        with open(analysis_file_name, "w") as analysis_results_file:
            json.dump(analysis_results, analysis_results_file, indent=4)

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
        characters_frequency = FreqDist(self.text.characters).most_common()
        return characters_frequency

    def get_characters_distribution(self):
        if not self.text.characters:
            return {}

        characters_distribution = {
            character: round(frequency * 100 / len(self.text.characters), 3)
            for character, frequency in self.get_characters_frequency()
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
        return self.get_words_frequency()[:number_of_words]

    def get_n_longest_words(self, number_of_words: int):
        return self.text.words[:number_of_words]

    def get_n_shortest_words(self, number_of_words: int):
        return self.text.words[:-number_of_words:-1]

    def get_n_longest_sentences(self, number_of_sentences):
        return self.text.sentences[:number_of_sentences]

    def get_n_shortest_sentences(self, number_of_sentences):
        return self.text.sentences[:-number_of_sentences:-1]

    def get_number_of_palindromes(self):
        return len(self.get_palindrome_words())

    def get_n_palindrome_words(self, number_of_words):
        palindrome_words = self.get_palindrome_words()
        return palindrome_words[:number_of_words] if palindrome_words else []

    def get_words_frequency(self):
        words_frequency = FreqDist(self.text.words).most_common()
        return words_frequency

    def get_palindrome_words(self):
        palindrome_words = [
            word
            for word in self.text.words
            if str(word).lower() == str(word).lower()[::-1]
        ]
        return palindrome_words

    def is_text_palindrome(self):
        return self.text.words == self.get_palindrome_words()

    def get_reversed_text(self, file_name):
        reversed_text = self.text.raw[::-1]
        reversed_text_file_name = f"reversed_{file_name}"

        with open(reversed_text_file_name, "w") as reversed_text_file:
            reversed_text_file.write(reversed_text)

        return reversed_text_file_name

    def get_reversed_text_with_characters_in_words_intact(self, file_name):
        reversed_text = self.text.raw[::-1]
        reversed_text_intact = " ".join([word[::-1] for word in reversed_text.split()])
        reversed_text_words_intact_file_name = f"reversed_words_intact_{file_name}"

        with open(
            reversed_text_words_intact_file_name, "w"
        ) as reversed_text_words_intact_file:
            reversed_text_words_intact_file.write(reversed_text_intact)

        return reversed_text_words_intact_file_name


def text_analyzer_runner(text_file_name):
    start_time = time.time()
    start_date_time_string = datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
    print(
        f"Report generation for {text_file_name} started at: {start_date_time_string}"
    )
    text = Text(text_file_name)
    text_analyzer = TextAnalyzer(text)
    analysis_result = text_analyzer.get_text_analysis()
    execution_time = (time.time() - start_time) * 1000
    print(analysis_result)
    print(f"The time taken to process the text (ms): {execution_time}")
    end_date_time_string = datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
    print(
        f"Report generated for {text_file_name} at (date and time): {end_date_time_string}"
    )
    return analysis_result


if __name__ == "__main__":
    text_files = [file for file in os.listdir() if file.endswith(".txt")]
    resource_names = [
        "http://www.textfiles.com/stories/bgcspoof.txt",
        "http://www.textfiles.com/stories/foxnstrk.txt",
        "http://www.textfiles.com/stories/hansgrtl.txt",
    ]

    with multiprocessing.Pool() as pool:
        pool.map(text_analyzer_runner, text_files)
