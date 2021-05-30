from PyQt5.QtWidgets import QApplication, QMainWindow,  QWidget 
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout   
from PyQt5.QtWidgets import QPushButton, QFileDialog, QCalendarWidget, QLabel, QComboBox
from PyQt5.QtCore import QObject, QThreadPool, pyqtSignal, QRunnable
from PyQt5 import QtCore, QtGui

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

import os, sys

import pandas as pd

import re

from JATS.JATS import *
from JATS.analyzer import Analyzer

import datetime
from datetime import timedelta

DATE_FORMAT = "yyyy-MM-dd"
base_dir = "data/tweets/"

active_thread_str = "There are {threads} running threads."

query = '"BTC" OR "bitcoin"'

class Signals(QObject):
    finished = pyqtSignal()
    
class Worker(QRunnable):
    signal = Signals()
    
    def set_date(self, date_from):
        self.date_from = date_from
    
    def run(self):
        get_tweets(query, self.date_from, self.date_from + timedelta(days=1), verbose = True)
        self.signal.finished.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.thread_count = 0
        
        self.setWindowTitle("My App")

        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setYRange(-1,1)
        
        button_menu_layout = QVBoxLayout()
        
        self.combo_sentiment_algorithm = QComboBox(self)
        self.combo_sentiment_algorithm.addItem("nltk")
        self.combo_sentiment_algorithm.addItem("textblob")
        
        self.sentiment_plot_button = QPushButton('Plot Sentiment')
        self.sentiment_plot_button.clicked.connect(self.load_graph)
        
        self.analyze_date_button = QPushButton('Analyze Day')
        self.analyze_date_button.clicked.connect(self.analyze_date)
        
        button_menu_layout.addWidget(self.combo_sentiment_algorithm)
        button_menu_layout.addWidget(self.sentiment_plot_button)
        button_menu_layout.addWidget(self.analyze_date_button)
        
        self.button_menu_container = QWidget()
        self.button_menu_container.setLayout(button_menu_layout)
        
        self.calendar = QCalendarWidget(self)
        self.set_calendar_color()
        
        top_layout = QGridLayout()
        top_layout.addWidget(self.button_menu_container, 1, 1)
        
        top_layout.addWidget(self.calendar, 1, 2)
        
        self.top_container = QWidget()
        self.top_container.setLayout(top_layout)
        
        self.thread_count_label = QLabel(active_thread_str.format(threads=str(self.thread_count)))
        
        layout = QVBoxLayout()
        layout.addWidget(self.top_container)
        layout.addWidget(self.graphWidget)
        layout.addWidget(self.thread_count_label)
        
        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)
        
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
    
    def set_calendar_color(self):
        """
            Colors the explored cells in the calendar
        """
        
        cell_format = QtGui.QTextCharFormat()
        cell_format.setBackground(QtGui.QColor("green"))

        
        for path in os.listdir( base_dir ):
            date = QtCore.QDate.fromString(path, DATE_FORMAT)

            if date.isValid():
                self.calendar.setDateTextFormat(date, cell_format)
    
    def load_graph(self):
        """
            Draw sentiment graph
        """
        
        selected_date =  self.calendar.selectedDate().toString(DATE_FORMAT)
        selected_algorithm = str(self.combo_sentiment_algorithm.currentText())
        
        
        directory = os.path.join(base_dir, selected_date)
        
        
        sentiment_file_name = os.path.join(base_dir, selected_date, "sentiment_file_" + selected_algorithm + ".csv")
        
        
        if not os.path.isfile(sentiment_file_name):
            tweet_file_name = os.path.join(base_dir, selected_date, "tweet_list.csv")
            
            tweet_df = pd.read_csv(tweet_file_name, sep=';')
            tweet_df["Datetime"] = pd.to_datetime(tweet_df["Datetime"])
            
            analyzer = Analyzer()
            analyzer.analyze(tweet_df, directory, algorithm=selected_algorithm)
            
        sentiment_df = pd.read_csv(sentiment_file_name, sep=';')
        
        sentiment_df["round_time"] = pd.to_datetime(sentiment_df["round_time"])

        self.graphWidget.clear()
        self.graphWidget.plot(sentiment_df.index, sentiment_df["sentiment"])

    def analyze_date(self):
        
        selected_date =  self.calendar.selectedDate().toPyDate()
        
        worker = Worker()
        worker.set_date(selected_date)
        worker.signal.finished.connect(self.refresh)
        
        self.threadpool.start(worker)
        self.refresh()
        
    def refresh(self):
        self.set_calendar_color()
        self.thread_count_label.setText(active_thread_str.format(threads=str(self.threadpool.activeThreadCount())))
        
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()