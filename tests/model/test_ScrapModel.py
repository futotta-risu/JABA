import pytest

from model.ScrapModel import ScrapModel


def test_scrapmodel_constructor():
    # Given

    # When
    try:
        ScrapModel()
        # Then
    except Exception:
        pytest.fail("Could not create ScrapModel")
        
def test_scrapmodel_setModelTypes():
    # Given
    scrap_model = ScrapModel()
    # When
    try:
        scrap_model.setModelTypes("Test")
        # Then
    except Exception:
        pytest.fail("Could not create ScrapModel")

def test_scrapmodel_createModelFrame():
    # Given
    scrap_model = ScrapModel()
    # When
    try:
        scrap_model.createModelFrame()
        # Then
    except Exception:
        pytest.fail("Could not create ScrapModel")