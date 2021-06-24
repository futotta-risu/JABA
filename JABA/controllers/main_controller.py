from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QRunnable
from PyQt5.QtCore import QThreadPool
from PyQt5.QtCore import QSettings

import pyqtgraph as pg
from pyqtgraph import PlotWidget

from service.scrapper.analyzer import Analyzer
from service.scrapper.cleaner import *
from service.scrapper.scrapper import *
from service.scrapper.ScrapService import ScrapService
from service.scrapper.bitcoin import BitcoinFileManager
from service.visualization.PlotService import PlotService
from views.plot_config import PlotConfigure

import pickle

from datetime import date



DATE_FORMAT = "yyyy-MM-dd"

INITIAL_DATE = QDate.fromString("2017-01-01", DATE_FORMAT)


base_dir = "data/tweets/"


class Signals(QObject):
    finished = pyqtSignal()
    
class AnalyzeDateWorker(QRunnable):
    '''
        Thread which scraps tweets and analyzes them. The thread need a date_from to work.
        
        Emits a finished signal in case of automatic scrapping.
    '''
    signal = Signals()
    
    def set_date(self, date_from):
        self.date_from = date_from
    
    def run(self):
        if self.date_from == None:
            raise Exception()
        
        scrapper = TwitterScrapper()
        analyzer = Analyzer()
        
        scrapper.scrap(self.date_from, self.date_from + timedelta(days=1), verbose=True)
        analyzer.analyze(self.date_from, ScrapperFileManager())

        self.signal.finished.emit()
        

class MainController(QObject):
    '''
        Controller for the main app window.
    '''
    def __init__(self, model):
        super().__init__()

        self._model = model

        self.plot_configurations = []
        self.plotService = PlotService()

        self.threadpool = QThreadPool()

        self._init_settings()
        
        self.scrapped_dates = set()
        self._get_scrapped_dates()

        
        

        

    def _init_settings(self):
        self.settings = QSettings("JABA", "JABA_Settings")
        try:
            self.settings.value("loaded_settings")
        except:
            self.settings.setValue("initial_date",
                                   QDate.fromString("2017-01-01", DATE_FORMAT))
            self.settings.setValue("loaded_settings", True)
            self.settings.sync()
            
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

    def get_analysis_methods(self):
        return Analyzer.get_algorithms()
    
    def _get_scrapped_dates(self):
        ''' Gets the date of the alredy scrapped dates and sets to scrapped_dates'''
        # Check if files inside folder or just folder
        
        for path in os.listdir( base_dir ):
            date = QDate.fromString(path, DATE_FORMAT)
            
            if date.isValid():
                self.scrapped_dates.add(date)
                
    def analyze_date(self, date):
        '''
            Loads the Analyze worker.
        '''
        worker = AnalyzeDateWorker()
        worker.set_date(date)
        worker.signal.finished.connect(self.automatic_scrapper)
        worker.signal.finished.connect(self._refresh_thread_count)
        
        self.threadpool.start(worker)
        
    def save_plot_config(self, file_name):
        with open(file_name, 'wb') as config_dictionary_file:
            plot_only_configs = [ptC['config'] for ptC in self.plot_configurations]
            pickle.dump(plot_only_configs, config_dictionary_file)
        
    def load_plot_config(self, file_name):
        with open(file_name, 'rb') as config_dictionary_file:
            return pickle.load(config_dictionary_file)
        

    def get_date_properties(self):
        date_list = []
        for path in os.listdir( base_dir ):
            date = QDate.fromString(path, DATE_FORMAT)
            
            if date.isValid():
                date_list += [[date, "data"]]

        return date_list
    
    def _refresh_thread_count(self):
        self._model.thread_count = self.threadpool.activeThreadCount()
    
    def automatic_scrapper(self):
        self._get_scrapped_dates()
        if not self._model.scrapping:
            return
        
        while self.actual_scrapper_date in self.scrapped_dates:
            self.actual_scrapper_date = self.actual_scrapper_date.addDays(1)
        
        if self.actual_scrapper_date >= date.today():
            return
        
        if self.threadpool.activeThreadCount() < 5:
            self.analyze_date(self.actual_scrapper_date.toPyDate())
            self.actual_scrapper_date = self.actual_scrapper_date.addDays(1) # Add day to avoid same day analyze
            self.automatic_scrapper()
            
    def get_message_sample_with_sentiment(self, date, algorithm, random = True):
        '''
            Returns a sample of the tweets with their respective sentiment.
        '''
        date = date.toString(DATE_FORMAT)
        tweet_file_name = os.path.join(base_dir, date, "tweet_list.csv")
            
        tweet_df = pd.read_csv(tweet_file_name, sep=';')
        
        
        
        if random:
            tweet_list = tweet_df.sample(n=50)
        else:
            tweet_list = tweet_df.sort_values('NumLikes', ascending = False).head(n=50)
        
        tweet_list = tweet_list["Text"]
        
        analyzer = Analyzer()
        
        tweets_text = [(clean_tweet(tweet_list.iloc[i])) for i in range(50)]
        return [(text, analyzer.get_sentiment(text)) for text in tweets_text]
        

    def create_plot(self, config):
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
            plotConfig = config_window.getPlotConfiguration()
            return self.create_plot(plotConfig)

        return None, "", None

    def update_plots(self, date, algorithm):
        plots = []
        
        scrapService = ScrapService()
        plotService = PlotService()

        for config in self.plot_configurations:
            id, pConfig, widget = config["id"], config["config"], config["widget"],
            
            args = {"date": date, "algorithm": algorithm }
            data = scrapService.get_data_by_category(pConfig.variable_type, args)
            
            index, data = plotService.applyPlotMaps(data, pConfig)
            
            widget.clear()
            widget.plot(index, data, pen=pg.mkPen('g', width=1))

