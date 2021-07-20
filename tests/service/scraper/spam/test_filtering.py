import pytest

import pandas as pd

from service.scraper.spam.filtering import filter_duplicated
from service.scraper.spam.filtering import filter_duplicated_pandas

from service.scraper.spam.filtering import filter_spam
from service.scraper.spam.filtering import filter_spam_concurrent

from unittest.mock import Mock

simple_example = [
    'Hi loved', 'Hi loved', 'Hi loved', 'Hi loved',
    'Hi loved', 'Hi loved', 'Hi loved', 'True Fact',
    'Non Fact'
]

def test_filter_duplicated():
    # Given
    data = simple_example

    # When
    result = filter_duplicated(data)

    # Then
    assert result.sort() == ['Hi loved', 'True Fact', 'Non Fact'].sort()

def test_filter_duplicated_pandas():
    # Given
    data = simple_example
    data_pandas = pd.DataFrame({'Text': data})
    # When
    result, spam = filter_duplicated_pandas(data_pandas)

    # Then
    assert result['Text'].to_list().sort() == ['Hi loved', 'True Fact', 'Non Fact'].sort()
    assert spam.iloc[0]['unique_texts'] == 'Hi loved'

def test_filter_duplicated_pandas_with_invalid_column():
    # Given
    data = simple_example
    data_pandas = pd.DataFrame({'Text': data})
    # When
    with pytest.raises(ValueError):
        filter_duplicated_pandas(data_pandas, column = 'Random')

def test_pandas_and_default_duplicate_are_same():
    # Given
    data = simple_example
    data_pandas = pd.DataFrame({'Text': data})
    # When
    result = filter_duplicated(data)
    result_pandas, _ = filter_duplicated_pandas(data_pandas)

    # Then
    assert result.sort() == result_pandas['Text'].to_list().sort()

def test_filter_spam():
    # Given
    data = simple_example

    # When
    result = filter_spam(data, verbose=True)

    # Then
    assert result == ['True Fact', 'Non Fact']

@pytest.mark.parametrize("batch_size", [-1, 0])
def test_filter_spam_fails_with_invalid_batch_size(batch_size):
    # Given
    data = simple_example

    # When
    with pytest.raises(ValueError):
        filter_spam(data, batch_size = batch_size)

def test_filter_spam_concurrent():
    # Given
    data = simple_example

    # When
    result = filter_spam_concurrent(data, batch_size=5)

    # Then
    assert result.sort() == ['True Fact', 'Non Fact'].sort()