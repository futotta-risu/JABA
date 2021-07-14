import pytest

from service.scraper.spam.filtering import filter_spam

from unittest.mock import Mock

import pandas as pd

def test_filter_spam():
    # Given
    data = [
        'Hi loved', 'Hi loved', 'Hi loved', 'Hi loved',
        'Hi loved', 'Hi loved', 'Hi loved', 'True Fact'
        ]

    # When
    result = filter_spam(data, verbose=True)

    # Then
    assert len(result) == 1