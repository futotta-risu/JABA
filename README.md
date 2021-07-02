# Just Another Bitcoin Analyzer (JABA)

* Dashboard for scrapping & tracking the twitter sentiment related with Bitcoin.
* Notebooks with Correlation Analysis & Forecasting with Facebook Prophet


## Status

* ![main](https://github.com/futotta-risu/JABA/actions/workflows/build.yml/badge.svg) 

* [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=futotta-risu_JABA&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=futotta-risu_JABA)
* [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=futotta-risu_JABA&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=futotta-risu_JABA)


## Execution

### 1. Install Requirements 
For executing the JABA app, first we need to download the necesary libraries using the requirements.txt file. Locate at the same level of the requirements file and execute next commands in your prompt:

    pip install -r requirements.txt
    python -m nltk.downloader names stopwords state_union twitter_samples movie_reviews averaged_perceptron_tagger vader_lexicon punkt

### 2. Run JABA app
Located inside the JABA folder and run the next command:

    python app.py
    
### 3. Scrap the DATA
Now you must see the dashboard of JABA empty, when you download the project the first time, you need to scrap the data needed for the analysis.
We give you 2 options:
1. Scrap the data starting by your preferred date\
    Select the date in the calendar and click **Data > Auto Scrap** in the menu

2. Use our prepared datasets\
    [Download It from Google Drive](https://drive.google.com/file/d/10Opisqx0QSxMW8jhUqEewXOEzMk9_sNK/view?usp=sharing)

Data must be located in daily folders inside the **data/bitcoin/YYYY-MM-DD** or **data/tweets/YYYY-MM-DD**, our data is grouped to 30m periods.

#### 3.1 SPAM filtering option
We have used clustering with DBSAN & Cosine Similarity for grouping similar tweets, and delete them if considered as SPAM.
This option can be activated in the [scrapper.py [Line 135]](https://github.com/futotta-risu/JABA/blob/main/JABA/service/scrapper/scrapper.py)
    
    tweets, spam_tweets = self.filter_spam(tweet_list, dbscan = True)

### 4. Plot daily data
You can select any day in the calendar and the sentiment and bitcoin price related plots will be updated to that day.
Furthermore, we can add, load or save plots to the dashboard with a high configurable options.
We can do this by clicking on the sections located in the submenu of **Plots**.
If we want to export or configure individually any of the displayed plots we only need to do right click on it.

### 5. Global Sentiment
We have been searching for a way to calculate a global sentiment caused by a tweet, taking into account more complex features, rather than the simple polarity offered by nltk.
The proposed formula for sentiment calculations is detailed in the [GlobalSentiment](https://github.com/futotta-risu/JABA/blob/main/GlobalSentiment.ipynb) notebook.

### 6. Forecasting With Prophet
We also have used the Facebook Prophet model for trying to forecast the future price of bitcoin given the sentiment of twitter. The analysis can be found in the [TSA](https://github.com/futotta-risu/JABA/blob/main/TSA.ipynb) notebook.
