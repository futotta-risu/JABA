import pytest

from service.scraper.ScrapService import ScrapService
from service.scraper.ScrapService import NoDataAvailableException

@pytest.mark.parametrize(
    "manager, data_type",
     [
         ('bitcoin.BitcoinFileManager.BitcoinFileManager', 'Bitcoin'),
         ('sentiment.SentimentFileManager.SentimentFileManager', 'Sentiment'),
         ('social.TweetFileManager.TweetFileManager', 'Tweet')
    ]
)
def test_get_data_by_category_tweet(mocker, manager, data_type):
    mock = mocker.patch('model.' + manager + '.open_file', return_value = None)

    service = ScrapService()
    service.get_data_by_category(data_type, {})

    mock.assert_called_once()

def test_get_data_by_category_raises(mocker):

    service = ScrapService()

    with pytest.raises(NoDataAvailableException):
        service.get_data_by_category('test_tipe', {})