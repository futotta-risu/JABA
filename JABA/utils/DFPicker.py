import pandas as pd
import numpy as np
from datetime import datetime, timezone
import time
import datetime
import re

def get_complete_df(dateFrom, dateTo):
    dateIterator = dateFrom
    final_df = pd.DataFrame()
    file_name_btc = "JABA/data/bitcoin/BTCUSDT-1m-data.csv"

    while(dateIterator != dateTo):
        file_name_sentiment = "JABA/data/tweets/" + str(dateIterator) + "/sentiment_file_nltk.csv"

        #try:
        if(final_df.shape[0] == 0):
            final_df = pd.read_csv(file_name_sentiment, sep=';')       
            final_df.drop(index = 1440, inplace = True)

            for i, time in enumerate(final_df["round_time"]):
                time = re.sub('\+\d\d\:\d\d', '', time)
                final_df.round_time[i] = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

            #final_df.drop(index=final_df.shape[0]-1, inplace = True)

        else:
            print(file_name_sentiment)
            temp_sentiment_df = pd.read_csv(file_name_sentiment, sep=';')
            temp_sentiment_df.drop(index = 1440, inplace = True)
            for i, time in enumerate(temp_sentiment_df["round_time"]):
                time = re.sub('\+\d\d\:\d\d', '', time)
                temp_sentiment_df.round_time[i] = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

            #final_df.drop(index=final_df.shape[0]-1, inplace = True)
            sentiment_frames = [temp_sentiment_df, final_df]
            final_df = pd.concat(sentiment_frames)

        #except:
            #print("Inexistent Date --> " , dateFrom)

        dateIterator += datetime.timedelta(days=1)

    temp_btc_df = pd.read_csv(file_name_btc, sep=",")
    temp_btc_df["round_time"] = pd.to_datetime(temp_btc_df["timestamp"])
    temp_btc_df.drop("timestamp", axis=1, inplace = True)

    temp_btc_df = temp_btc_df[(temp_btc_df["round_time"] >= pd.to_datetime(dateFrom)) & (temp_btc_df["round_time"] < pd.to_datetime(dateTo))]

    final_df.insert(1, "Trades", temp_btc_df["trades"].values, True)
    final_df.insert(1, "Close", temp_btc_df["close"].values, True)
    final_df.insert(1, "Low", temp_btc_df["low"].values, True)
    final_df.insert(1, "High", temp_btc_df["high"].values, True)
    final_df.insert(1, "Open", temp_btc_df["open"].values, True)

    return final_df