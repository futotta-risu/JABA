import pandas as pd

class Sentiment:
    
    column_names = [
        'round_time',
        'sentiment'
    ]
    
    def setModelTypes(self, df):
        df["round_time"] = pd.to_datetime(df["round_time"])
        df["sentiment"] = pd.to_numeric(df["sentiment"]) 

        return df
    
    def createModelFrame(self):
        return self.setModelTypes(pd.DataFrame(columns = self.column_names))