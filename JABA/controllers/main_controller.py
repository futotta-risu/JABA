from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QRunnable
from PyQt5.QtCore import QThreadPool

import pyqtgraph as pg
from pyqtgraph import PlotWidget

from service.scrapper.analyzer import Analyzer
from service.scrapper.cleaner import *
from service.scrapper.scrapper import *
from service.scrapper.ScrapService import ScrapService
from service.scrapper.bitcoin import BitcoinFileManager

from service.visualization.PlotService import PlotService
from views.plot_config import PlotConfigure

DATE_FORMAT = "yyyy-MM-dd"

INITIAL_DATE = QDate.fromString("2017-01-01", DATE_FORMAT)

base_dir = "data/tweets/"

from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QThreadPool


DATE_FORMAT = "yyyy-MM-dd"

INITIAL_DATE = QDate.fromString("2017-01-01", DATE_FORMAT)


base_dir = "data/tweets/"


query = '"BTC" OR "bitcoin"'


query = '"BTC" OR "bitcoin"'

class Signals(QObject):
    finished = pyqtSignal()
    
class AnalyzeDateWorker(QRunnable):
    signal = Signals()
    
    def set_date(self, date_from):
        self.date_from = date_from
    
    def run(self):
        scrapper = TwitterScrapper()
        analyzer = Analyzer()
        
        scrapper.scrap(self.date_from, self.date_from + timedelta(days=1), verbose=True)
        analyzer.analyze(self.date_from, ScrapperFileManager())

        self.signal.finished.emit()
        

class MainController(QObject):
    def __init__(self, model):
        super().__init__()


        self._model = model

        self.plot_configurations = []

        self.plotService = PlotService()

        self.threadpool = QThreadPool()

        self.actual_scrapper_date = QDate.fromString("2017-01-01", DATE_FORMAT)

        self.scrapped_dates = set()
        self._get_scrapped_dates()


        self.settings = QSettings("JABA", "JABA_Settings")

        try:
            self.settings.value("loaded_settings")
        except:
            self._init_settings()

        

    def _init_settings(self):
        self.settings.setValue("initial_date",
                               QDate.fromString("2017-01-01", DATE_FORMAT))
        self.settings.setValue("loaded_settings", True)
        self.settings.sync()

    def set_settings(self, new_settings):
        self.settings = new_settings
        self.actual_scrapper_date = self.settings.value("initial_date")
        self.settings.sync()

    def get_settings(self):
        return self.settings

    def _init_local_vars(self):
        self.actual_scrapper_date = self.settings.value("initial_date",
                                                        type=QDate)

    def _get_scrapped_dates(self):
        for path in os.listdir( base_dir ):
            date = QDate.fromString(path, DATE_FORMAT)
            
            if date.isValid():
                self.scrapped_dates.add(date)
                
    def analyze_date(self, date):
        
        worker = AnalyzeDateWorker()
        worker.set_date(date)
        worker.signal.finished.connect(self.automatic_scrapper)
        worker.signal.finished.connect(self._refresh_thread_count)
        
        self.threadpool.start(worker)
        
        
        
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
        
        if self.threadpool.activeThreadCount() < 5:
            self.analyze_date(self.actual_scrapper_date.toPyDate())
            self.actual_scrapper_date = self.actual_scrapper_date.addDays(1) # Add day to avoid same day analyze
            self.automatic_scrapper()
            
    def get_message_sample_with_sentiment(self, date, algorithm):
        
        date = date.toString(DATE_FORMAT)
        directory = os.path.join(base_dir, date)
        tweet_file_name = os.path.join(base_dir, date, "tweet_list.csv")
            
        tweet_df = pd.read_csv(tweet_file_name, sep=';')
        
        tweets = []

        tweet_list = tweet_df.sort_values('NumLikes', ascending = False).head(n=50)
        tweet_list = tweet_list["Text"]


        analyzer = Analyzer()
        
        for i in range(50):
            text = tweet_list.iloc[i]
            text = clean_tweet(text)
            sentiment = analyzer.get_sentiment(text) 
            tweets += [(text, sentiment)]


    def open_configure(self):
        config_window = PlotConfigure(self)
        config_window.show()
        config_window.exec_()

        if config_window.is_saved():
            plotConfig = config_window.getPlotConfiguration()
            widget = PlotWidget()
            id = self.plotService.getPlotID()
            self.plot_configurations += [{
                "id": id,
                "config": plotConfig,
                "widget": widget
            }]

            return id, plotConfig.name, widget

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

