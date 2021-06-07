from .scrapper import *



query = '"BTC" OR "bitcoin"'

class NoDataAvailableException(Exception):
    pass

class ScrapService:
    
    def get_data_by_category(self, dataModel, args):
        data = None
        if dataModel == "Tweet":
            data = get_tweet_from_file(args["date"])
        else:
            raise NoDataAvailableException("No data detected")
        
        return data