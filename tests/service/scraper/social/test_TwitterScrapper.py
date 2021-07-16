import pytest

from service.scraper.social.TwitterScraper import TwitterScraper

from snscrape.modules.twitter import Tweet, User

from unittest.mock import Mock

import pandas as pd

import datetime

def test_TwitterScrapper_constructor():
    # Given
    # When
    try:
        TwitterScraper()
    except Exception:
        pytest.fail("Could not create Twitter Scraper")

def get_random_tweet():
    return Tweet(
        'url', 
        datetime.datetime.now(),
        'content',
        'renderedContent',
        122345,
        User('user',2),
        3,
        4,5,6,7, 'en','source')

def test_TwitterScrapper_scrap(mocker):
    # Given
    file_manager = Mock()
    file_manager.file_exists.return_value = False
    file_manager.save_file.return_value = None
    
    scraper = TwitterScraper()
    scraper.set_file_manager(file_manager)

    tweet = get_random_tweet()


    mocker.patch('snscrape.modules.twitter.TwitterSearchScraper.get_items',return_value=[tweet, tweet])

    # When
    scraper.scrap(datetime.datetime.now())

    file_manager.save_file.assert_called_once()


def test_TwitterScrapper_scrap_limit(mocker):
    # Given
    file_manager = Mock()
    file_manager.file_exists.return_value = False
    file_manager.save_file.return_value = None
    
    scraper = TwitterScraper()
    scraper.set_file_manager(file_manager)

    tweet = get_random_tweet()


    mocker.patch('snscrape.modules.twitter.TwitterSearchScraper.get_items',return_value=[tweet, tweet, tweet])

    # When
    scraper.scrap(datetime.datetime.now(), limit=2)

    file_manager.save_file.assert_called_once()

def test_TwitterScrapper_scrap_existent_file(mocker):
    # Given
    file_manager = Mock()
    file_manager.file_exists.return_value = True
    file_manager.save_file.return_value = None
    
    scraper = TwitterScraper()
    scraper.set_file_manager(file_manager)

    # When
    scraper.scrap(datetime.datetime.now())

    file_manager.save_file.assert_not_called()
