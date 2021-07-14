import pytest

from service.scraper.spam.metrics import jacard, soronsen, overlap

from unittest.mock import Mock

import numpy as np

def test_jacard():
    # Given
    test_text_1 = np.array(['I am Test']).reshape(-1,1)
    test_text_2 = np.array(['I am Tost']).reshape(-1,1)
    
    # When
    result = jacard(test_text_1[0], test_text_2[0])

    # Then
    assert pytest.approx(result, 0.1) == 2/4

def test_soronsen():
    # Given
    test_text_1 = np.array(['I am Test']).reshape(-1,1)
    test_text_2 = np.array(['I am Tost']).reshape(-1,1)
    
    # When
    result = soronsen(test_text_1[0], test_text_2[0])

    # Then
    assert pytest.approx(result, 0.1) == 1/3

def test_overlap():
    # Given
    test_text_1 = np.array(['I am Test']).reshape(-1,1)
    test_text_2 = np.array(['I am Tost']).reshape(-1,1)
    
    # When
    result = overlap(test_text_1[0], test_text_2[0])

    # Then
    assert pytest.approx(result, 0.1) == 1/3

