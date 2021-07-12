import pickle

from datetime import date
from pathlib import Path

import random
import time

import os

import pandas as pd

from PyQt5.QtCore import QDate
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QThreadPool
from PyQt5.QtCore import QSettings

from pyqtgraph import PlotWidget

from service.scraper.worker.DateScrapWorker import DateScrapWorker
from service.scraper.sentiment.analyzer import Analyzer
from service.scraper.cleaner import clean_tweet

from service.visualization.PlotService import PlotService
from gui.view.plot_config import PlotConfigure

from loguru import logger

DATE_FORMAT = "yyyy-MM-dd"

INITIAL_DATE = QDate.fromString("2017-01-01", DATE_FORMAT)

base_dir = "data/tweets/"


class MainController(QObject):
    '''
        Controller for the main app window.
    '''

    scrapped_dates = set()

    def __init__(self, model):
        super().__init__()

        self._model = model

        self.plot_configurations = []
        self.plotService = PlotService()

        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(self._model.max_threads)

        self._init_settings()

        self._get_scrapped_dates()

    def _init_settings(self):
        logger.debug("Loading settings.")

        self.settings = QSettings("JABA", "JABA_Settings")
        try:
            self.settings.value("loaded_settings")

        except BaseException:
            logger.warning("Settings were not loaded. Creating new settings.")

            self.settings.setValue("initial_date",
                                   QDate.fromString("2017-01-01", DATE_FORMAT))
            self.settings.setValue("loaded_settings", True)
            self.settings.setValue("analysis_algorithm", 'nltk')
            self.settings.sync()

        logger.success("Settings loaded.")
        self.load_settings()

    def set_settings(self, new_settings):
        self.settings = new_settings
        self.load_settings()
        self.settings.sync()

    def load_settings(self):
        ''' Load controller variables from settings'''
        self.actual_scrapper_date = self.settings.value("initial_date", type=QDate)

    def get_settings(self):
        return self.settings

    def get_analysis_method(self):
        return self.settings.value("analysis_algorithm")

    def get_analysis_methods(self):
        return Analyzer.get_algorithms()

    def _get_scrapped_dates(self):
        ''' Gets the date of the alredy scrapped dates and sets to scrapped_dates'''
        # TODO Move function to it's own file manager
        Path(base_dir).mkdir(parents=True, exist_ok=True)

        for path in os.listdir(base_dir):
            date = QDate.fromString(path, DATE_FORMAT)

            if date.isValid():
                self.scrapped_dates.add(date)

    def save_plot_config(self, file_name):
        ''' Save Plot configurations to custom plot file '''

        logger.debug(f"Dumping plot configurations to {file_name}.")
        with open(file_name, 'wb') as config_dictionary_file:
            plot_only_configs = [ptC['config'] for ptC in self.plot_configurations]
            pickle.dump(plot_only_configs, config_dictionary_file)

    def load_plot_config(self, file_name):
        ''' Load plot configurations from custom plot file '''

        logger.debug(f"Loading plot configurations from {file_name}.")
        with open(file_name, 'rb') as config_dictionary_file:
            return pickle.load(config_dictionary_file)

    def get_dates(self):
        dates = [QDate.fromString(path, DATE_FORMAT) for path in os.listdir(base_dir)]
        return [date for date in dates if date.isValid()]

    def change_automatic_scrapper(self):
        self._model.auto_scraping = not self._model.auto_scraping

    def getScrapDate(self):
        while self.actual_scrapper_date in self.scrapped_dates:
            self.actual_scrapper_date = self.actual_scrapper_date.addDays(1)

        if self.actual_scrapper_date >= date.today():
            print(self.actual_scrapper_date)
            raise Exception()

        return self.actual_scrapper_date

    def startAutoScrapWorker(self):
        self._model.auto_scraping = True

        while self.threadpool.activeThreadCount() < self._model.max_threads:
            logger.info("Starting new scrap worker.")
            self.startScrapWorker()

    def startScrapWorker(self, date=None):
        ''' Gets a new  ScrapWorker and launches it '''
        time.sleep(random.uniform(0, 0.2))
        if self.threadpool.activeThreadCount() >= self._model.max_threads:
            return

        if date is None:
            if self._model.auto_scraping:
                date = self.getScrapDate()
            else:
                return

        self.scrapped_dates.add(date)

        worker = DateScrapWorker()
        worker.set_date(date.toPyDate())
        worker.signal.finished.connect(self.startScrapWorker)

        self.threadpool.start(worker)

    def stopAutoScrap(self):
        self._model.auto_scraping = False

    def get_message_sample_with_sentiment(self, date, algorithm, random=True):
        '''
            Returns a sample of the tweets with their respective sentiment.
        '''

        logger.info(f"Getting sample for {date.toPyDate()} and {algorithm}.")

        # TODO Replace location of this function
        date = date.toString(DATE_FORMAT)
        tweet_file_name = os.path.join(base_dir, date, "tweet_list.csv")

        tweet_df = pd.read_csv(tweet_file_name, sep=';')

        if random:
            tweet_list = tweet_df.sample(n=50)
        else:
            tweet_list = tweet_df.sort_values('NumLikes', ascending=False).head(n=50)

        tweet_list = tweet_list["Text"]

        analyzer = Analyzer()

        tweets_text = [(clean_tweet(tweet_list.iloc[i])) for i in range(50)]
        return [(text, analyzer.get_sentiment(text)) for text in tweets_text]

    def create_plot(self, config):
        ''' Creates a plot widget and id and adds it to the plot configuration list '''
        widget = PlotWidget()
        id = self.plotService.getPlotID()
        self.plot_configurations += [{
            "id": id,
            "config": config,
            "widget": widget
        }]

        return id, config.name, widget

    def open_configure(self):
        config_window = PlotConfigure(self)
        config_window.show()
        config_window.exec_()

        if config_window.is_saved():
            logger.success("Plot created from configuration.")
            plotConfig = config_window.getPlotConfiguration()
            return self.create_plot(plotConfig)

        logger.warning("Plot configuration window closed without saving. Data is discarded")
        return None, "", None

    def update_plots(self, date, algorithm):
        ''' Refreshes the plots from a certain date and algorithm '''

        plotService = PlotService()
        plotService.updatePlots(self.plot_configurations, date, algorithm)

    def get_plots(self):
        return self.plot_configurations

    def delete_plot(self, id):
        # TODO Replace list to hashmap for speed
        self.plot_configurations = [x for x in self.plot_configurations if x['id'] != id]
