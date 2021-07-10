import pytest

import pandas as pd

from model.bitcoin.BitcoinFileManager import BitcoinFileManager

def test_create_tweet_file_manager():
    bitcoinFileManager = BitcoinFileManager()
    
    assert bitcoinFileManager != None

    
def test_get_file_name():
    # Given
    bitcoinFileManager = BitcoinFileManager()
    args = {'date' : '2021-01-13'}
    
    # When
    file_name = bitcoinFileManager.get_file_name(args)
    
    # Then
    assert file_name == "data/bitcoin/2021-01-13\\bitcoin.csv" or file_name == "data/bitcoin/2021-01-13/bitcoin.csv"
    
def test_get_file_name_fails_on_no_date():
    # Given
    bitcoinFileManager = BitcoinFileManager()
    args = {}
    
    # When
    try:
        file_name = bitcoinFileManager.get_file_name(args)
        
        # Then
        pytest.fail("Should not return name")
    except Exception:
        assert True
    
    
def test_open_file(mocker):
    # When
    data = pd.DataFrame(columns = ['timestamp', 'Close'])
    args = {'date' : '2021-01-13'}
    
    bitcoinFileManager = BitcoinFileManager()
    
    mocker.patch('pandas.read_csv', return_value=data) 
    
    try:
        # When
        data = bitcoinFileManager.open_file(args)
        
        # Then
        assert True
    except Exception:
        pytest.fail("Open File")
    
def test_open_file_raises_on_non_existent_file(mocker):
    # When
    data = pd.DataFrame(columns = ['Datetime'])
    args = {'date' : '2021-01-13'}
    
    bitcoinFileManager = BitcoinFileManager()
    
    mocker.patch('pandas.read_csv', return_value=Exception()) 
    
    try:
        # When
        data = bitcoinFileManager.open_file(args)
        
        # Then
        pytest.fail("File should not exist")
    except Exception:
        assert True
    
def test_open_file_raises_on_invalid_columns(mocker):
    # When
    data = pd.DataFrame(columns = ['Datetim'])
    args = {'date' : '2021-01-13'}
    
    bitcoinFileManager = BitcoinFileManager()
    
    mocker.patch('pandas.read_csv', return_value=data) 
    
    try:
        # When
        data = bitcoinFileManager.open_file(args)
        
        # Then
        pytest.fail("File should not exist")
    except Exception:
        assert True