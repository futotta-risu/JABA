import pytest

from service.scraper.sentiment.analyzer import Analyzer

from unittest.mock import Mock

def test_analyzer_contructor():
    # Given
    # When
    try:
        Analyzer()
        # Then
    except Exception:
        pytest.fail("Analyzer cannot be constructed")

def test_analyzer_get_sentiment_nltk():
    # Given
    analyzer = Analyzer()
    # When
    result = analyzer.get_sentiment("I love you", algorithm="nltk")

    # Then
    assert result > 0

def test_analyzer_get_sentiment_text_blob():
    # Given
    analyzer = Analyzer()
    # When
    result = analyzer.get_sentiment("I love you", algorithm="textblob")

    # Then
    assert result > 0

def test_analyzer_get_sentiment_None():
    # Given
    analyzer = Analyzer()
    # When
    try:
        result = analyzer.get_sentiment("I love you", algorithm=None)

        # Then
        pytest.fail("Analyzer with None should raise Exception")
    except Exception:
        assert True

def test_analyzer_get_sentiment_none_existent():
    # Given
    analyzer = Analyzer()
    # When
    try:
        result = analyzer.get_sentiment("I love you", algorithm="randomTest33")

        # Then
        pytest.fail("Analyzer with None should raise Exception")
    except Exception:
        assert True
