# Just Another Bitcoin Analyzer (JABA)

Dashboard for social network sentiment tracking.

| Description        | Status           | 
| ------------- |:-------------:| 
| Main Build & Test      | ![main](https://github.com/futotta-risu/JABA/actions/workflows/build.yml/badge.svg) | 
| Development Build & Test    | ![development](https://github.com/futotta-risu/JABA/actions/workflows/build.yml/badge.svg?branch=development)      | 


## Execution

Run 

    python -m pip install --upgrade pip
    pip install -r requirements.txt
    python -m nltk.downloader all
    pip3 install git+https://github.com/JustAnotherArchivist/snscrape.git
    python app.py


## Incoming Changes


- [ ] Add a spam filtering system
- [ ] Create a model to predict price movements based on sentiment
- [ ] Improve the tweet gathering system to avoid duplicate dates
- [ ] Custom dashboard settings
- [ ] Generate config file for data Scrapping Config
- [x] Add a view of Scrapping Config
- [x] Add visual interface to the library
- [x] Change the code from a notebook to python files and leave the notebook as a visual tool/tutorial


## Changelog

* (25/05/2021) Added methods to analyze sentiment with NLTK
* (23/05/2021) Added methods to scrap tweets
* (05/06/2021) Added methos for clustering similar tweets

