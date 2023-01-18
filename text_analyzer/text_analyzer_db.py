from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, JSON, BOOLEAN, select


engine = create_engine("sqlite:///text_analyzer.db", echo=True)
meta = MetaData()

text_analysis_table = Table(
    "text_analysis", meta,
    Column("id", Integer, primary_key=True),
    Column("File name", String, key="file_name"),
    Column("Generation time", DateTime, key="generation_time"),
    Column("The number of paragraphs", Integer, key="paragraphs"),
    Column("The number of sentences", Integer, key="sentences"),
    Column("The number of words", Integer, key="words"),
    Column("The number of characters", Integer, key="characters"),
    Column("Frequency of characters", JSON, key="characters_frequency"),
    Column("Distribution of characters", JSON, key="characters_distribution"),
    Column("The average word length", Integer, key="avg_word_length"),
    Column("The average number of words in a sentence", Integer, key="avg_words_in_sentence"),
    Column("Top 10 most used words", JSON, key="most_used_words"),
    Column("Top 10 longest words", String, key="longest_words"),
    Column("Top 10 shortest words", String, key="shortest_words"),
    Column("Top 10 longest sentences", String, key="longest_sentences"),
    Column("Top 10 shortest sentences", String, key="shortest_sentences"),
    Column("The number of palindrome words", Integer, key="number_of_palindromes"),
    Column("Top 10 longest palindrome words", String, key="longest_palindromes"),
    Column("Is the whole text a palindrome", BOOLEAN, key="is_text_palindrome"),
    Column("Is the all words in text palindromes", BOOLEAN, key="is_all_words_are_palindromes"),
    Column("Reversed text saved to", String, key="reversed_text_filename"),
    Column("Reversed text with the characters order in the words kept intact saved to", String,
           key="reversed_with_order_filename"),
)


meta.create_all(engine)


def get_report_view(file_name):
    stmt = select(text_analysis_table).where(text_analysis_table.c.file_name == file_name)

    with engine.connect() as connection:
        for row in connection.execute(stmt).mappings():
            for column, value in row.items():
                print(f"{column.upper()}: {value}")
