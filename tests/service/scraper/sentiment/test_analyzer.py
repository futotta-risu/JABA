import pytest

from service.scraper.sentiment.analyzer import Analyzer

from unittest.mock import Mock

import pandas as pd

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

def test_analyzer_analyze():
    # Given
    analyzer = Analyzer()

    args = {'sentiment':[0,0], 'Text':["I love you", "Love"]}
    data= pd.DataFrame(args)
    
    file_manager = Mock()
    file_manager.open_file.return_value = data
    file_manager.save_file.return_value = None

    # When
    try:
        result = analyzer.get_sentiment('2010-02-03', file_manager)

        # Then
        pytest.fail("Analyzer with None should raise Exception")
    except Exception:
        assert True

