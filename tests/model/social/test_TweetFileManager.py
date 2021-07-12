import pytest

import pandas as pd

from model.social.TweetFileManager import TweetFileManager


def test_create_tweet_file_manager():
    try:
        TweetFileManager()
    except Exception:
        pytest.fail("Could not create TweetFileManager")


def test_get_file_name():
    # Given
    tweetFileManager = TweetFileManager()
    args = {'date': '2021-01-13'}

    # When
    file_name, spam_file_name = tweetFileManager.get_file_name(args)

    # Then
    assert file_name == "data/tweets/2021-01-13/tweet_list.csv"
    assert spam_file_name == "data/tweets/2021-01-13/spam_tweet_list.csv"


def test_get_file_name_fails_on_no_date():
    # Given
    tweetFileManager = TweetFileManager()
    args = {}

    # When
    try:
        file_name, spam_file_name = tweetFileManager.get_file_name(args)

        # Then
        pytest.fail("Should not return name")
    except Exception:
        assert True


def test_open_file(mocker):
    # When
    data = pd.DataFrame(columns=['Datetime'])
    args = {'date': '2021-01-13'}

    tweetFileManager = TweetFileManager()

    mocker.patch('pandas.read_csv', return_value=data)

    try:
        # When
        data = tweetFileManager.open_file(args)

        # Then
        assert True
    except Exception:
        pytest.fail("Pandas error")


def test_open_file_raises_on_non_existent_file(mocker):
    # When
    args = {'date': '2021-01-13'}

    tweetFileManager = TweetFileManager()

    mocker.patch('pandas.read_csv', return_value=Exception())

    try:
        # When
        tweetFileManager.open_file(args)

        # Then
        pytest.fail("File should not exist")
    except Exception:
        assert True


def test_open_file_raises_on_invalid_columns(mocker):
    # When
    data = pd.DataFrame(columns=['Datetim'])
    args = {'date': '2021-01-13'}

    tweetFileManager = TweetFileManager()

    mocker.patch('pandas.read_csv', return_value=data)

    try:
        # When
        tweetFileManager.open_file(args)

        # Then
        pytest.fail("File should not exist")
    except Exception:
        assert True


def test_file_exists_returns_true_on_existent(mocker):
    # When
    tweetFileManager = TweetFileManager()

    mocker.patch('os.path.isfile', return_value=True)

    # When
    data = tweetFileManager.file_exists(date='2021-01-13')

    # Then
    assert data


def test_file_exists_returns_true_on_non_existent(mocker):
    # When
    tweetFileManager = TweetFileManager()

    mocker.patch('os.path.isfile', return_value=False)

    # When
    data = tweetFileManager.file_exists(date='2021-01-13')

    # Then
    assert not data


def test_file_exists_fails_on_non_valid_date(mocker):
    # When
    tweetFileManager = TweetFileManager()
    mocker.patch('os.path.isfile', return_value=True)

    try:
        # When
        tweetFileManager.file_exists(None)

        # Then
        pytest.fail("Invalid type should not be accepted")
    except TypeError:
        assert True
