import pytest

from app import App

from unittest.mock import Mock

import sys

def test_app_constructor(mocker):
    # Given    
    mocker.patch('os.listdir', return_value=['2017/02/02', '2017/02/03', '2017/42/03'])

    # When
    try:
        App(sys.argv)
        # Then
    except Exception:
        pytest.fail("Could not create App")
