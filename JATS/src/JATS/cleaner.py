import re
import emoji

from nltk.corpus import stopwords

def clean_tweet(tweet):
    """
        Clean function for tweets.
        
        The function applies the next steps:
            - Lower text
            - Clean usernames. E.g. @erik.tr
            - Clean http links
            - Remove hashtag or dollar but keep the text
            - Replace ; with ,
            - Delete non word characters
            - Remove extra whitespaces
            - Remove stopwods
        
        Parameter:
        tweet (string)
        
        Returns:
        Cleaned tweet
        
    """
    tweet = tweet.lower()
    tweet = re.sub("@[A-Za-z0-9_]+","",tweet) #Remove user (e.g. @erik.tr)
    tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet) #Remove http links
    tweet = emoji.get_emoji_regexp().sub(r'', tweet)
    tweet = tweet.replace("#", "").replace("\\$", "").replace("_", " ") #Remove hashtag or dollar sign but keep the text
    tweet = tweet.replace(";", ".")
    tweet = re.sub(r'[\W., ]', ' ', tweet) # Delete non word tokens
    tweet = " ".join(tweet.split()) # Remove extra whitespaces
    tweet = " ".join([word for word in tweet.split() if word not in stopwords.words('english')])
    
    return tweet