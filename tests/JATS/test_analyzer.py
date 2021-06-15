import pytest 
import numpy as np

from JABA.JATS.analyzer import *

a = Analyzer()

def test_get_sentiment_positive(): 
    assert a.get_sentiment("I am very happy because Bitcoin is growing up") >= 0.5
    
def test_get_sentiment_negative(): 
    assert a.get_sentiment("I am very afraid of the Bitcoin price changes, i think i am going to lose all my money by taking this risk") <= -0.5 
    
def test_get_sentiment_neutral(): 
    sentiment = a.get_sentiment("Hi, my name is Lander") 
    assert sentiment <= 0.5 
    assert sentiment >= -0.5

# TODO: Crear este test
def test_analyze():
    a = None

def test_get_cosine_similarity():
    cleaned_texts = ['BILBAO', 'BILBAO', 'MADRID', 'MADRD', 'VALENCIA']
    expected_array = np.array([
                        [1,1,0,0,0],
                        [1,1,0,0,0],
                        [0,0,1,0,0],
                        [0,0,0,1,0],
                        [0,0,0,0,1]
                      ])
    csim = a.get_cosine_similarity(cleaned_texts)
    comparison = csim == expected_array
    assert comparison.all() == True
