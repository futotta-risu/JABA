import re

from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer

emoji_pattern = re.compile(
    "["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    u"\U0001F1F2-\U0001F1F4"  # Macau flag
    u"\U0001F1E6-\U0001F1FF"  # flags
    u"\U0001F600-\U0001F64F"
    u"\U00002702-\U000027B0"
    u"\U000024C2-\U0001F251"
    u"\U0001f926-\U0001f937"
    u"\U0001F1F2"
    u"\U0001F1F4"
    u"\U0001F620"
    u"\u200d"
    u"\u2640-\u2642"
    "]+",
    flags=re.UNICODE,
)

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
        - Deletes emojis
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

    # We don't use the emoji library since its really slow
    tweet = emoji_pattern.sub(r"", tweet)
    tweet = " ".join(tweet.split())

    return tweet


def total_clean(text):
    text = decontracted(text)
    text = " ".join([w for w in text.split() if not w in stop_words])
    return re.sub(r"[\W.,:() ]", " ", text)
