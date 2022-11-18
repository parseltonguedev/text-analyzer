from setuptools import setup, find_packages

setup(
    name="text-analyzer",
    version="1.0.0",
    author="Bohdan Solianyk",
    author_email="solyanik.py@gmail.com",
    packages=find_packages(),
    requires=[
        "click",
        "requests",
        "validators",
        "nltk",
    ]
)
