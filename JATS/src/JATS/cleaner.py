import re
import emoji

def clean_tweet(tweet):
    tweet = re.sub("@[A-Za-z0-9_]+","",tweet) #Remove @ sign
    tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet) #Remove http links
    tweet = " ".join(tweet.split())
    tweet = emoji.get_emoji_regexp().sub(r'', tweet)
    tweet = tweet.replace("#", "").replace("_", " ") #Remove hashtag sign but keep the text
    tweet = tweet.replace(";", ".")
    return tweet