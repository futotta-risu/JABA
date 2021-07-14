import pytest

from app import App

from unittest.mock import Mock

import sys

def test_app_constructor(mocker):
    # Given    
    mocker.patch('pandas.DataFrame.to_csv', return_value=None)

    # When
    try:
        App(sys.argv)
        # Then
    except Exception:
        pytest.fail("Could not create App")
