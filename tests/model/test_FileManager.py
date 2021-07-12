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

def test_file_manager_get_name_not_invalid():
    # Given
    file_manager = FileManagerInterface()
    # When
    try:
        file_manager.get_file_name({})
        # Then
    except Exception:
        pytest.fail("Could not create get name")
        
def test_file_manager_open_file_not_invalid():
    # Given
    file_manager = FileManagerInterface()
    # When
    try:
        file_manager.open_file({})
        # Then
    except Exception:
        pytest.fail("Could not create open file")
        
def test_file_manager_save_file_not_invalid():
    # Given
    file_manager = FileManagerInterface()
    # When
    try:
        file_manager.save_file([], {})
        # Then
    except Exception:
        pytest.fail("Could not save file")
