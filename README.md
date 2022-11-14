# Text Analyzer

## TODO:

- [x] top longest and shortest sentences words concatenation to correct string format
- [x] leave only unique palindrome words in list and number of them
- [x] improve time calculation for data processing
- [x] make reversed text with intact words correct output
- [x] make correct string join for list of strings (i.e. remove whitespaces before symbols)
- [x] make more pretty report time generation 
- [x] add support UTF8 encoding text
- [ ] add CLI support with click:
  * help -h
  * multiple local file names -f
  * multiple web resources files -r
- [ ] investigate multiprocessing and threading to process multiple files at the same time
- [ ] add logging with structure:
  * date|type of resource|filename or resource name|event(info,warning, critical)
- [ ] add error handling (for example, binary file or failed to connect to server)
- [ ] add setup.py file to build with sdist command or install using pip