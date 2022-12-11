from setuptools import setup, find_packages

setup(
    name="textanalyzertool",
    version="1.0.1",
    author="Bohdan Solianyk",
    author_email="solyanik.py@gmail.com",
    description="Tool to analyze text from local text files or web resources. "
                "You can analyze several texts simultaneously.",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "requests",
        "validators",
        "nltk",
    ],
    python_requires=">=3.11",
    zip_safe=False
)
