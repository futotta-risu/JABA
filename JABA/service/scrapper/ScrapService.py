from .scrapper import *
from .analyzer import *


query = '"BTC" OR "bitcoin"'


class NoDataAvailableException(Exception):
    pass


class ScrapService:

    def get_data_by_category(self, dataModel, args):
        data = None
        if dataModel == "Tweet":
            scrapper = ScrapperFileManager()
            data = scrapper.open_file(args)
        elif dataModel == "Sentiment":
            fileManager = AnalyzerFileManager()
            data = fileManager.open_file(args)
        else:
            raise NoDataAvailableException("No data detected")

        return data
