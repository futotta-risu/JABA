import pytest

from JABA.JATS.cleaner import *

def test_clean_tweet_lowers_case():
	
	assert clean_tweet("Hi, im Erik") == "hi, im erik","Problem while cleaning tweet"