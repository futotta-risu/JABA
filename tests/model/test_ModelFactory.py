import pytest

from model.ModelFactory import createModelFrame

from unittest.mock import Mock

import sys

def test_createModelFrame_with_valid_object(mocker):
    # Given 

    # When
    try:
        createModelFrame('Bitcoin')
        # Then
    except Exception:
        pytest.fail("Could not create model")

def test_createModelFrame_with_invalid_object(mocker):
    # Given 

    # When
    try:
        createModelFrame('Bitcoin2')
        # Then
        pytest.fail("Could create invalid model")
    except Exception:
        pass

def test_createModelFrame_with_None(mocker):
    # Given 

    # When
    try:
        createModelFrame(None)
        # Then
        pytest.fail("Could create invalid model")
    except Exception:
        pass
