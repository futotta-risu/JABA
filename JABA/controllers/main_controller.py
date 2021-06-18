from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QRunnable
from PyQt5.QtCore import QThreadPool
from pyqtgraph import PlotWidget
from service.scrapper.analyzer import Analyzer
from service.scrapper.cleaner import *
from service.scrapper.scrapper import *
from service.scrapper.ScrapService import ScrapService
from service.visualization.PlotService import PlotService
from views.plot_config import PlotConfigure

DATE_FORMAT = "yyyy-MM-dd"

INITIAL_DATE = QDate.fromString("2017-01-01", DATE_FORMAT)


base_dir = "data/tweets/"


query = '"BTC" OR "bitcoin"'


class Signals(QObject):
    finished = pyqtSignal()


class AnalyzeDateWorker(QRunnable):
    signal = Signals()

    def set_date(self, date_from):
        self.date_from = date_from

    def run(self):
        get_tweets(
            query, self.date_from, self.date_from + timedelta(days=1), verbose=True
        )
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

    def _get_scrapped_dates(self):
        for path in os.listdir(base_dir):
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
        for path in os.listdir(base_dir):
            date = QDate.fromString(path, DATE_FORMAT)

            if date.isValid():
                date_list += [[date, "data"]]

        return date_list

    def get_sentiment_plot_data(self, date, algorithm):
        """
        Returns the index and sentiment column of a date
        """

        date = date.toString(DATE_FORMAT)
        directory = os.path.join(base_dir, date)

        sentiment_file_name = os.path.join(
            base_dir, date, "sentiment_file_" + algorithm + ".csv"
        )
        sentiment_tweet_file_name = os.path.join(
            base_dir, date, "tweet_sentiment_" + algorithm + ".csv"
        )

        if not os.path.isfile(sentiment_file_name):
            tweet_file_name = os.path.join(base_dir, date, "tweet_list.csv")

            tweet_df = pd.read_csv(tweet_file_name, sep=";")
            tweet_df["Datetime"] = pd.to_datetime(tweet_df["Datetime"])

            analyzer = Analyzer()
            analyzer.analyze(tweet_df, directory, algorithm=algorithm, verbose=True)

        sentiment_df = pd.read_csv(sentiment_file_name, sep=";")

        sentiment_df["round_time"] = pd.to_datetime(sentiment_df["round_time"])

        sentiment_dist = pd.read_csv(sentiment_tweet_file_name, sep=";")

        sentiment_dist = sentiment_dist[sentiment_dist["sentiment"] != 0]
        sentiment_dist["sentiment"] = sentiment_dist["sentiment"].round(1)

        total_vals = sentiment_dist.shape[0]
        sentiment_dist = sentiment_dist.groupby("sentiment").agg({"sentiment": "count"})

        sentiment_dist["sentiment"] = sentiment_dist["sentiment"] / total_vals

        return (
            sentiment_df.index,
            sentiment_df["sentiment"],
            sentiment_dist.index.tolist(),
            sentiment_dist["sentiment"].tolist(),
        )

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
            self.actual_scrapper_date = self.actual_scrapper_date.addDays(
                1
            )  # Add day to avoid same day analyze
            self.automatic_scrapper()

    def get_message_sample_with_sentiment(self, date, algorithm):

        date = date.toString(DATE_FORMAT)
        directory = os.path.join(base_dir, date)
        tweet_file_name = os.path.join(base_dir, date, "tweet_list.csv")

        tweet_df = pd.read_csv(tweet_file_name, sep=";")

        tweets = []

        tweet_list = tweet_df["Text"].sample(n=50)

        analyzer = Analyzer()

        for i in range(50):
            text = tweet_list.iloc[i]
            text = clean_tweet(text)
            sentiment = analyzer.get_sentiment(text)
            tweets += [(text, sentiment)]

        return tweets

    def get_plot_data(self, dataCategory, plotConfig, args):
        """
        Returns the scrapped data prepared to be plotted
        """

        if "date" in args:
            args["date"] = args["date"].toString(DATE_FORMAT)

        scrapService = ScrapService()
        data = scrapService.get_data_by_category(dataCategory, args)

        plotService = PlotService()
        return plotService.prepareData(data, plotConfig)

    def open_configure(self):
        config_window = PlotConfigure(self)
        config_window.show()
        config_window.exec_()

        if config_window.is_saved():
            plotConfig = config_window.getPlotConfiguration()
            widget = PlotWidget()
            id = self.plotService.getPlotID()
            self.plot_configurations += [
                {"id": id, "config": plotConfig, "widget": widget}
            ]

            return id, widget

        return None, None

    def update_plots(self, date, algorithm):
        plots = []

        scrapService = ScrapService()
        plotService = PlotService()

        for plot_config in self.plot_configurations:
            id, plotConfig, widget = (
                plot_config["id"],
                plot_config["config"],
                plot_config["widget"],
            )

            data = scrapService.get_data_by_category(
                plotConfig.variable_type, {"date": date, "algorithm": algorithm}
            )

            print(data.head())

            index, data = plotService.applyPlotMaps(data, plotConfig)
            widget.clear()
            widget.plot(index, data)
