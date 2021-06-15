import pytest 

from JABA.JATS.analyzer import * 

def test_get_sentiment_positive(): 
    assert get_sentiment("I am very happy because Bitcoin is growing up") > 1
    
def test_get_sentiment_negative(): 
    assert get_sentiment("I am very afraid of the Bitcoin price changes, i think i am going to lose all my money") < 0 
    
def test_get_sentiment_neutral(): 
    sentiment = get_sentiment("Hi, my name is Lander") 
    assert sentiment <= 0.5 
    assert sentiment >= -0.5