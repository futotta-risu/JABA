# Just Another Bitcoin Analyzer (JABA)

Dashboard for tracking the twitter sentiment related with Bitcoin.


## Status

* Main Build & Test: ![main](https://github.com/futotta-risu/JABA/actions/workflows/build.yml/badge.svg) 

* [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=futotta-risu_JABA&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=futotta-risu_JABA)
* [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=futotta-risu_JABA&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=futotta-risu_JABA)


## Execution

### 1. Install Requirements 
For executing the JABA app, first we need to download the necesary libraries using the requirements.txt file.

    pip install -r requirements.txt
    python -m nltk.downloader names stopwords state_union twitter_samples movie_reviews averaged_perceptron_tagger vader_lexicon punkt

### 2. Run JABA app
Located inside the JABA folder, run the next command:

    python app.py
    
### 3. Scrap the DATA
When you download the project the first time, you need to scrap the data needed for the analysis
Select the scrapper **Start Date** in the configuration menu, then...

### 4. Plot daily data
You can select any day in the calendar and the sentiment and bitcoin price related plots will be updated to that day.

### More info in the wiki

