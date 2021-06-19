import pytest

from JABA.service.scrapper import cleaner

def test_clean_tweet_lowers_case():
	
	assert cleaner.clean_tweet("Hi, im Erik") == "hi, im erik","Problem while cleaning tweet"