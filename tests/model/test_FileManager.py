import pytest

import pandas as pd

from model.FileManager import FileManagerInterface

def test_create_file_manager():
    fileManager = FileManagerInterface()
    
    assert fileManager != None

    