import pandas as pd


class Bitcoin:

    column_names = [
        "timestamp_round",
        "timestamp",
        "close",
        "volume",
    ]

    def setModelTypes(self, df):
        df["timestamp_round"] = pd.to_datetime(df["timestamp_round"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["close"] = pd.to_numeric(df["close"])
        df["volume"] = pd.to_numeric(df["volume"])

        return df

    def createModelFrame(self):
        return self.setModelTypes(pd.DataFrame(columns=self.column_names))
