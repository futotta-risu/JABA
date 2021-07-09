from model.sentiment.SentimentFileManager import SentimentFileManager
from model.bitcoin.BitcoinFileManager import BitcoinFileManager
from model.social.TweetFileManager import TweetFileManager

query = '"BTC" OR "bitcoin"'

class NoDataAvailableException(Exception):
    pass

class ScrapService:
    def get_data_by_category(self, dataModel, args):
        ''' Returns the data based on the data model. '''
        
        if dataModel == "Tweet":
            fileManager = TweetFileManager()
        elif dataModel == "Sentiment":
            fileManager = SentimentFileManager()
        elif dataModel == "Bitcoin":
            fileManager = BitcoinFileManager()
        else:
            raise NoDataAvailableException("No data detected")
        
        data = fileManager.open_file(args)
        return data
