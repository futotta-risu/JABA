import pytest

from log import start_log


def test_app_constructor():
    # Given    
    # When
    try:
        start_log()
        # Then
    except Exception:
        pytest.fail("Could not create log")
