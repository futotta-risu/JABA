from math import ceil
from multiprocessing import Pool
import time

from sklearn.cluster import DBSCAN
from scipy.spatial.distance import pdist, squareform

import numpy as np
import pandas as pd

from .metrics import jacard

def chunks(lst, n):
    """
        Yield successive n-sized chunks from lst.

        https://stackoverflow.com/questions/312443
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def filter_duplicated(data : list):
    '''
        Filters the duplicated elements from the data.

        Parameters:
            data (list) List of strings.
    '''
    return list(dict.fromkeys(data))

def filter_duplicated_pandas(
    data : pd.DataFrame,
    column : str = "Text"
    ):
    '''
        Filters the duplicated elements from the data and return cleaned data and duplicates.

        Parameters:
            data (pd.DataFrame) DataFrame
    '''
    if column not in data.columns:
        raise ValueError("Column must be in dataframe to use it in the filtering.")

    data = data[(data["Text"].notna()) & data["Text"]] # Remove Nan's

    duplicated_counts = data[data["Text"].duplicated()]["Text"].value_counts()
    data_spam = duplicated_counts.rename_axis("unique_texts").reset_index(name="counts")

    data.drop_duplicates(subset="Text", keep='first', inplace=True)

    return data, data_spam

def filter_spam_batch(batch : list, metric = jacard, eps : float =0.3):
    ''' Filters spam batch based on text similarity '''
    batch = np.array(batch).reshape(-1, 1)
    distance_matrix = squareform(pdist(batch, metric))
    db = DBSCAN().fit(distance_matrix)

    return [batch[i] for i, cat in enumerate(db.labels_) if cat == -1]


# TODO Implement version for pandas
def filter_spam(
    data : list, 
    batch_size : int = 5000,
    verbose : bool = False,
    metric = jacard,
    eps : float = 0.3):
    '''
        Filters spam based on text similarity.

        Parameters
            data : Python list of the input data. The list can be a string.
    '''
    if batch_size < 1:
        raise ValueError("Batch size must be a positive integer")

    batches = ceil(len(data)/batch_size)

    filtered_data = []

    if verbose:
        
        start_time = time.time()

    for n_batch in range(batches):
        if verbose:
            last_batch_time = time.time() - start_time
            start_time = time.time()

            eta_time = (batches + 1 - n_batch) * last_batch_time

            batch_output = f'Current batch {n_batch+1} of {batches}.'
            time_output = 'ETA : %i:%2i' % (eta_time//60, int(eta_time) % 60)
            print(batch_output + ' ' + time_output)

        batch = data[batch_size * n_batch:batch_size * (n_batch+1)]

        filtered_data += filter_spam_batch(batch, metric = metric, eps = eps)
        

    return filtered_data



def filter_spam_concurrent(data,  batch_size : int = 5000, verbose=False, metric=jacard, eps=0.3):
    ''' Filters spam from data based on text similarity concurrently '''
    if batch_size < 1:
        raise ValueError("Batch size must be a positive integer")

    batches = chunks(data, batch_size)
    del data

    result_data = []

    with Pool(5) as pool:
        result_data = pool.map(filter_spam_batch, batches)

    return result_data