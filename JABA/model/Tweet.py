import pandas as pd


class Tweet:

    column_names = [
        "Datetime",
        "Tweet Id",
        "Text",
        "NumReplies",
        "NumRetweets",
        "NumLikes",
        "IDOriginalRetweeted",
        "Username",
        "isVerified",
    ]

    def setModelTypes(self, df):
        df["Text"] = df["Text"].astype("str")
        df["Datetime"] = pd.to_datetime(df["Datetime"])
        df["NumReplies"] = pd.to_numeric(df["NumReplies"])
        df["NumRetweets"] = pd.to_numeric(df["NumRetweets"])
        df["NumLikes"] = pd.to_numeric(df["NumLikes"])
        df["Username"] = df["Username"].astype("str")

        return df

    def createModelFrame(self):
        return self.setModelTypes(pd.DataFrame(columns=self.column_names))
