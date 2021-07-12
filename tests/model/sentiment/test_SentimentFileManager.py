import pytest

import pandas as pd

from model.sentiment.SentimentFileManager import SentimentFileManager


def test_create_tweet_file_manager():
    try:
        SentimentFileManager()
    except Exception:
        pytest.fail("Could not create SentimentFileManager")


def test_get_file_name_fails_on_no_date():
    # Given
    sentimentFileManager = SentimentFileManager()

    # When
    try:
        sentimentFileManager.get_file_name({})

        # Then
        pytest.fail("Should not return name")
    except Exception:
        assert True


def test_open_file_raises_on_non_existent_file(mocker):
    # When
    args = {'date': '2021-01-13'}

    sentimentFileManager = SentimentFileManager()

    mocker.patch('pandas.read_csv', return_value=Exception())

    try:
        # When
        sentimentFileManager.open_file(args)

        # Then
        pytest.fail("File should not exist")
    except Exception:
        assert True


def test_open_file_raises_on_invalid_columns(mocker):
    # When
    data = pd.DataFrame(columns=['Datetim'])
    args = {'date': '2021-01-13'}

    sentimentFileManager = SentimentFileManager()

    mocker.patch('pandas.read_csv', return_value=data)

    try:
        # When
        sentimentFileManager.open_file(args)

        # Then
        pytest.fail("File should not exist")
    except Exception:
        assert True
