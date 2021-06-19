from .file_manager import FileManagerInterface

import os
from pathlib import Path
import pandas as pd

class BitcoinFileManager(FileManagerInterface):
    def __init__(self):
        super().__init__()
        self.DIRECTORY = "data/bitcoin/{day}"
        self.FILE_NAME = os.path.join(self.DIRECTORY, "bitcoin.csv")

    def get_file_name(self, args: dict):
        return self.FILE_NAME.format(day=args["date"])

    def open_file(self, args: dict):
        """
        Returns the dataframe from the scrapper class
        """
        
        file_name = self.get_file_name(args)
        data = pd.read_csv(file_name, sep=";")
        
        data["timestamp"] = pd.to_datetime(data["timestamp"])

        return data

    def save_file(self, data, args: dict):
        """
        Saves the file if it doesn't exist
        """
        file_name = self.get_file_name(args)

        Path(self.DIRECTORY).mkdir(parents=True, exist_ok=True)
        data.to_csv(file_name, sep=";", index=False)
