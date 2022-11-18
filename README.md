# Text Analyzer

Text sources:
- https://sherlock-holm.es/ascii/
- https://www.cl.cam.ac.uk/~mgk25/ucs/examples/UTF-8-demo.txt

## TODO:

- [x] top longest and shortest sentences words concatenation to correct string format
- [x] leave only unique palindrome words in list and number of them
- [x] improve time calculation for data processing
- [x] make reversed text with intact words correct output
- [x] make correct string join for list of strings (i.e. remove whitespaces before symbols)
- [x] make more pretty report time generation 
- [x] add support UTF8 encoding text
- [x] add CLI support with click:
  * help (python main.py --help)
  * Usage: main.py [OPTIONS] [FILE_NAMES]...
  * Example with local text file: python main.py file1.txt
  * Example with local text files: python main.py file1.txt file2.txt file3.txt
  * Example with web resource: python main.py
  https://www.cl.cam.ac.uk/~mgk25/ucs/examples/UTF-8-demo.txt
  * Example with web resources: python main.py https://www.cl.cam.ac.uk/~mgk25/ucs/examples/UTF-8-demo.txt https://sherlock-holm.es/stories/plain-text/advs.txt https://sherlock-holm.es/stories/plain-text/sign.txt https://sherlock-holm.es/stories/plain-text/scan.txt
- [ ] investigate multiprocessing and threading to process multiple files at the same time
- [x] add logging with structure:
  * date|type of resource|filename or resource name|event(info,warning, critical)
- [x] add error handling (for example, binary file or failed to connect to server)
- [x] add setup.py file to build with sdist command or install using pip:
  * python setup.py sdist
  * It is important to remember, however, that running this file as a script (e.g. python setup.py sdist) 
    is strongly discouraged, and that the majority of the command line interfaces are (or will be) deprecated (e.g. python setup.py install, python setup.py bdist_wininst, …).
    We also recommend users to expose as much as possible configuration in a more declarative way via the pyproject.toml or setup.cfg, and keep the setup.py minimal with only the dynamic parts (or even omit it completely if applicable).
- [ ] investigate setup.cfg or pyproject.toml


## Issues:

1. Using multiprocessing and urlopen raise this issue with some resources links:
    ```
    multiprocessing.pool.MaybeEncodingError: Error sending result: '<multiprocessing.pool.ExceptionWithTraceback object at 0x7f7e68b0a690>'. Reason: 'TypeError("cannot pickle '_io.BufferedReader' object")'
    ```
    
    To avoid this issue I changed **urllib** to **requests** library to get web text documents from web resources
