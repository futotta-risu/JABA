import pytest

from gui.component.table.SentimentTable import SentimentTable


def test_sentimenttable_constructor(qtbot):
    # Given
    # When
    try:
        SentimentTable()
        # Then
    except Exception:
        pytest.fail("Could not create Sentiment Table")


def test_sentimenttable_add_row(qtbot):
    # Given
    container = SentimentTable()

    # When
    try:
        container.addRow("Text", 0.4)
        # Then
    except Exception:
        pytest.fail("Sentiment Table addRow should not raise.")
