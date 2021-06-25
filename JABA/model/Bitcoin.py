import pandas as pd

from .ScrapModel import ScrapModel

class Bitcoin(ScrapModel):
    
    name = "Bitcoin"
    
    column_names = [
        "round_datetime",
        "timestamp",
        "Close"
    ]

    def setModelTypes(self, df):
        df["round_datetime"] = pd.to_datetime(df["round_datetime"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["Close"] = pd.to_numeric(df["Close"])

        return df

    def createModelFrame(self):
        return self.setModelTypes(pd.DataFrame(columns=self.column_names))
