import re

from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer

stop_words = set(stopwords.words("english"))
stop_words.remove('not')

def decontracted(phrase):
    '''https://stackoverflow.com/questions/19790188'''
    # specific
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase

def clean_tweet(tweet):
    """
    Clean function for tweets.

    The function applies the next steps:
        - Lowers text
        - Deletes ;
        - Deletes urls
        - Deletes # and $ without deleting text
        - Deletes users
        - Deletes extra whitehouses

    Parameter:
    tweet (string)

    Returns:
    Cleaned tweet

    """
    tweet = tweet.lower()
    tweet = tweet.replace(";", ".")
    tweet = (tweet.replace("#", "").replace("$", "").replace("_", " ")
             )  # Remove hashtag or dollar sign but keep the text
    tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "",
                   tweet)  # Remove http links
    tweet = re.sub(r"@\S+", "", tweet)

    tweet = re.sub(r"(-?)[0-9][0-9,\.]+(%?)", "", tweet)

    tweet = " ".join(tweet.split())

    return tweet


def total_clean(text):
    text = decontracted(text)
    text = " ".join([w for w in text.split() if not w in stop_words])
    return re.sub(r"[\W.,:() ]", " ", text)
