import pytest

from app import App
from PyQt5.QtWidgets import QMainWindow

import sys

def test_app_create(mocker):
    mocker.patch('PyQt5.QtWidgets.QMainWindow.show', return_value=None) 
    
    app = App(sys.argv)
    
    assert app is not None