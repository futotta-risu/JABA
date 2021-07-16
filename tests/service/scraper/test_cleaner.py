import pytest


from service.scraper import cleaner


def test_decontracted():
    # Given
    text = "I'm not you"
    # When
    result = cleaner.decontracted(text)
    
    # Then
    assert result == 'I am not you'

def test_clean_tweet():
    # Given
    text = "I'm not you http://www.erik.com"
    # When
    result = cleaner.clean_tweet(text)
    
    # Then
    assert result == 'i\'m not you'

def test_total_clean():
    # Given
    text = "I'm not you :3 :D )()"
    # When
    result = cleaner.total_clean(text)
    
    # Then
    assert result == 'I not  3  D    '
    
