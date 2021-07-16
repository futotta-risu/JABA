import pytest

from gui.model.MainWindowModel import MainWindowModel


def test_mainwindowmodel_constructor(qtbot):
    # Given

    # When
    try:
        MainWindowModel()
        # Then
    except Exception:
        pytest.fail("Could not create MainWindowModel")


def test_max_threads_get(qtbot):
    # Given
    model = MainWindowModel()

    # When
    max_threads = model.max_threads

    # Then
    assert max_threads == 12


def test_auto_scraping_get(qtbot):
    # Given
    model = MainWindowModel()

    # When
    auto_scraping = model.auto_scraping

    # Then
    assert not auto_scraping


def test_auto_scraping_set(qtbot):
    # Given
    model = MainWindowModel()

    # When
    model.auto_scraping = True

    # Then
    assert model.auto_scraping
