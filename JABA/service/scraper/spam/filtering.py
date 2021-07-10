from math import ceil

from sklearn.cluster import DBSCAN
from scipy.spatial.distance import pdist, squareform

import numpy as np

from .metrics import jacard_t

def filter_duplicated(data):
    ''' 
        Filters the duplicated elements from the data.
        
        Parameters:
            data (list) List of strings.
    '''
    pass # TODO Implement functions


def filter_spam(data, batch_size = 5000, verbose = False, metric = jacard_t, eps = 0.3):
    ''' 
        Filters spam based on text similarity.
        
        Parameters
            data : Python list of the input data. The list can be a string.
    '''
    batches = ceil(len(data)/batch_size)

    filtered_data = []

    if verbose:
        import time
        start_time = time.time()
        
    for n_batch in range(batches):
        if verbose:
            last_batch_time =  time.time() - start_time
            start_time = time.time()
            
            eta_time = (batches + 1 - n_batch ) * last_batch_time 
            
            batch_output = f'Current batch {n_batch+1} of {batches}.' 
            time_output = 'ETA : %i:%2i' % ( eta_time//60, int(eta_time)%60 )
            print(batch_output + ' ' + time_output)
            
        batch = data[batch_size * n_batch:batch_size * (n_batch+1)]

        batch  = np.array(batch).reshape(-1,1)
        distance_matrix = squareform(pdist(batch, metric))
        db = DBSCAN().fit(distance_matrix)
                    
        for i,v in enumerate(db.labels_):
            if v == -1:
                filtered_data += [batch[i]]
                
    return filtered_data
