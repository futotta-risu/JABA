# Just Another Bitcoin Analyzer (JABA)
![main](https://github.com/futotta-risu/JABA/actions/workflows/build.yml/badge.svg) 
Dashboard for scrapping & tracking the twitter sentiment related with Bitcoin.

![GIF demo](https://miro.medium.com/max/700/1*5KJpHcwmNoxVHmkHipyL4g.gif)

## Installation
To use JABA, you will need to download the repo and install the requirements

    pip install -r requirements.txt

once you have the necessary imports, you will need to exec the app

    python JABA/app.py
    
## Data Scraping
JABA is planned to have the option to scrap the data when needed, but the project isn't finished, and we don't have this option yet for all the data. The data scraping is divided in social network and bitcoin:

* **Social network** can be downloaded through the autoscrap option in the app menu. 
* **Bitcoin** data is not yet automatically scraped, so we have uploaded the current data to this [url](https://drive.google.com/file/d/1Kjs9CpYB9ueGJubsrQwnoURdhw78GTXY/view?usp=sharing). The bitcoin folder extracted from the zip file must be located in the /JABA/data/ folder.

## Global Sentiment
The main academic proposal from this repository is a different sentiment analysis formula for sets of texts. Exploring the field, the most common proporsal has been to apply the mean to the list of sentiments. We reject this vision since it doesn't hold enough information about the list.

The details of it can be seen in the notebook [GlobalSentiment](https://github.com/futotta-risu/JABA/blob/main/GlobalSentiment.ipynb).

## Future Lines
We plan to update the project adding new features. The main lines in which we will be working are:
* Custom search queries apart from Bitcoin, accessible from the app.
* Online database from AWS.
* Multiday plot visualization
