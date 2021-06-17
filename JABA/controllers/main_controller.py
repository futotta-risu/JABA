from JATS.analyzer import Analyzer
from JATS.cleaner import *
from JATS.JATS import *
from PyQt5.QtCore import (QDate, QObject, QRunnable, QSettings, QThreadPool,
                          pyqtSignal, pyqtSlot)

DATE_FORMAT = "yyyy-MM-dd"

base_dir = "data/tweets/"
base_dir_btc = "data/bitcoin/"

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

        self.settings = QSettings("JABA", "JABA_Settings")

        try:
            self.settings.value("loaded_settings")
        except:
            self._init_settings()

        self._model = model

        self._init_local_vars()

        self.threadpool = QThreadPool()

        self.scrapped_dates = set()
        self._get_scrapped_dates()

    def _init_settings(self):
        self.settings.setValue(
            "initial_date", QDate.fromString("2017-01-01", DATE_FORMAT)
        )
        self.settings.setValue("loaded_settings", True)
        self.settings.sync()

    def set_settings(self, new_settings):
        self.settings = new_settings
        self.actual_scrapper_date = self.settings.value("initial_date")
        self.settings.sync()

    def get_settings(self):
        return self.settings

    def _init_local_vars(self):
        self.actual_scrapper_date = self.settings.value("initial_date", type=QDate)

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

        print(sum(sentiment_dist["sentiment"]))
        return (
            sentiment_df.index,
            sentiment_df["sentiment"],
            sentiment_dist.index.tolist(),
            sentiment_dist["sentiment"].tolist(),
        )

    def get_btc_price_plot_data(self, date, plotType):
        """
        Returns the subset of the bitcoin historial dataset given a date for creating a chart
        """
        btc_df = self.get_btc_price_subdf(date)

        return (
            btc_df.index,
            btc_df["timestamp"],
            range(0, btc_df.shape[0]),
            btc_df[plotType].tolist(),
        )

    def get_btc_price_subdf(self, date):
        """
        Returns the subset of the bitcoin historial dataset given a date
        """
        nextDay = date.addDays(1).toString(DATE_FORMAT)
        date = date.toString(DATE_FORMAT)
        directory = os.path.join(base_dir_btc, date)

        bitcoin_dataset_file_name = os.path.join(base_dir_btc, "BTCUSDT-1m-data.csv")

        btc_df = pd.read_csv(bitcoin_dataset_file_name, sep=",")

        btc_df["timestamp"] = pd.to_datetime(btc_df["timestamp"])

        btc_df = btc_df[(btc_df.timestamp >= date) & (btc_df.timestamp < nextDay)]

        return btc_df

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
