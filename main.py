import multiprocessing
import os
import time
from datetime import datetime

from nltk import FreqDist
from nltk.corpus import PlaintextCorpusReader, stopwords
from nltk.tokenize import regexp_tokenize


def main(file_name):
    start_time = time.time()

    current_folder = os.getcwd()

    stop_words = set(stopwords.words("english"))

    file_corpus_reader = PlaintextCorpusReader(current_folder, file_name)

    raw_text = file_corpus_reader.raw()
    text_paragraphs = file_corpus_reader.paras()
    text_sentences = file_corpus_reader.sents()
    text_words = file_corpus_reader.words()
    text_characters = [character for word in text_words for character in word]

    tokenized_sentences = [
        [
            word
            for word in regexp_tokenize(" ".join(sentence), r"\w+")
            if word.lower() not in stop_words
        ]
        for sentence in text_sentences
    ]
    tokenized_sentences = [sentence for sentence in tokenized_sentences if sentence]

    tokenized_text_characters = [
        char for sentence in tokenized_sentences for word in sentence for char in word
    ]

    tokenized_text_words = sorted(
        [
            word
            for sentence in tokenized_sentences
            for word in sentence
            if len(word) >= 2
        ],
        key=len,
        reverse=True,
    )

    characters_frequency = FreqDist(text_characters).most_common()
    tokenized_characters_frequency = FreqDist(tokenized_text_characters).most_common()

    characters_distribution = {
        character: round(frequency * 100 / len(text_characters), 3)
        for character, frequency in characters_frequency
    }
    tokenized_characters_distribution = {
        character: round(frequency * 100 / len(tokenized_text_characters), 3)
        for character, frequency in tokenized_characters_frequency
    }

    average_word_length = round(
        sum((len(word) for word in text_words)) / len(text_words)
    )
    average_tokenized_word_length = round(
        sum((len(word) for word in tokenized_text_words)) / len(tokenized_text_words)
    )

    number_of_words_in_a_sentence = round(
        sum((len(sentence) for sentence in text_sentences)) / len(text_sentences)
    )
    number_of_words_in_tokenized_sentence = round(
        sum((len(sentence) for sentence in tokenized_sentences))
        / len(tokenized_sentences)
    )

    words_frequency = FreqDist(text_words).most_common()
    tokenized_words_frequency = FreqDist(tokenized_text_words).most_common()

    sentences_sorted_by_length = sorted(
        [sentence for sentence in text_sentences], key=len, reverse=True
    )
    palindrome_words = sorted(
        [
            word
            for word in tokenized_text_words
            if str(word).lower() == str(word).lower()[::-1]
        ],
        key=len,
        reverse=True,
    )

    reversed_text = raw_text[::-1]
    reversed_text_list = reversed_text.split()
    reversed_with_order = " ".join([word[::-1] for word in reversed_text_list])

    current_date_time_string = datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
    execution_time = (time.time() - start_time) * 1000

    print(f"The number of characters: {len(text_characters)}")
    print(f"The number of characters (tokenized): {len(tokenized_text_characters)}")
    print(f"The number of paragraphs: {len(text_paragraphs)}")
    print(f"The number of words: {len(text_words)}")
    print(f"The number of words (tokenized): {len(tokenized_text_words)}")
    print(f"The number of sentences: {len(text_sentences)}")
    print(f"The number of sentences (tokenized): {len(tokenized_sentences)}")
    print(f"Frequency of characters: {characters_frequency}")
    print(f"Frequency of characters (tokenized): {tokenized_characters_frequency}")
    print(f"Distribution of characters: {characters_distribution}")
    print(f"Distribution of characters (tokenized) {tokenized_characters_distribution}")
    print(f"Average word length: {average_word_length}")
    print(f"Average word length (tokenized): {average_tokenized_word_length}")
    print(f"The average number of words in a sentence {number_of_words_in_a_sentence}")
    print(
        f"The average number of words in a sentence (tokenized): {number_of_words_in_tokenized_sentence}"
    )
    print(f"Top 10 most used words: {words_frequency[:10]}")
    print(f"Top 10 most used words (tokenized): {tokenized_words_frequency[:10]}")
    print(f"Top 10 longest words:")
    for word in tokenized_text_words[:10]:
        print(word)
    print(f"Top 10 shortest words:")
    for word in reversed(tokenized_text_words[-10:]):
        print(word)
    print(f"Top 10 longest sentences:")
    for sentence in sentences_sorted_by_length[:10]:
        print(" ".join(sentence))
    print(f"Top 10 shortest sentences:")
    for sentence in reversed(sentences_sorted_by_length[-10:]):
        print(" ".join(sentence))
    print(f"Number of palindrome words: {len(palindrome_words)}")
    print(f"Top 10 longest palindrome words:")
    for palindrome in palindrome_words[:10]:
        print(palindrome)
    print(f"Is the whole text a palindrome: {palindrome_words == tokenized_text_words}")
    print(f"Reversed text: {reversed_text}")
    print(
        f"Reversed text but the character order in words kept intact: {reversed_with_order}"
    )
    print(f"The time taken to process the text (ms): {execution_time}")
    print(
        f"Report generated for {file_name} at (date and time): {current_date_time_string}"
    )


if __name__ == "__main__":
    text_files = [file for file in os.listdir() if file.endswith(".txt")]

    with multiprocessing.Pool(len(text_files)) as pool:
        pool.map(main, text_files)
