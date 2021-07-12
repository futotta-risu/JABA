import pytest

from model.FileManager import FileManagerInterface


def test_create_file_manager():
    # Given

    # When
    try:
        FileManagerInterface()
        # Then
    except Exception:
        pytest.fail("Could not create FileManagerInterface")
