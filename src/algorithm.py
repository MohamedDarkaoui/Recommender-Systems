from pathlib import Path
import random
import numpy as np
import scipy.sparse

import typer

import Algorithms.src.util as util
from Algorithms.src.algorithm.algorithm import Algorithm

from Algorithms.src.cross_validation.strong_generalization import strong_generalization
from Algorithms.src.cross_validation.weak_generalization import weak_generalization
from Algorithms.src.metric.recall import recall_k


PathArgument = typer.Argument(
    ...,
    exists=True,
    file_okay=True,
    dir_okay=False,
    writable=False,
    readable=True,
    resolve_path=True,
    help="A readable file."
)


AMOUNT_TEST_USERS = 5
SEED = 5

def return_run(alg: Algorithm, X: scipy.sparse.csr_matrix):
    """ Train a model and show the recommendations for random users. """
    random.seed(SEED)
    np.random.seed(SEED)

    alg.fit(X)
    return alg

def wmf(dataframe, alpha: float = 40.0, factors: int = 20, regularization: float = 0.01, iterations: int = 20, train=None):
    """ Train and predict with the WMF model. """
    from Algorithms.src.algorithm.wmf import WMF

    alg = WMF(alpha=alpha, num_factors=factors, regularization=regularization, iterations=iterations)
    X = None
    if train == None:
        X = util.df_to_csr(dataframe)
    else:
        X = train
    return return_run(alg, X)

def ease(dataframe, l2: float = 200.0, train=None):
    """ Train and predict with the EASE model. """
    from Algorithms.src.algorithm.ease import EASE
    

    alg = EASE(l2=l2)
    X = None
    if train == None:
        X = util.df_to_csr(dataframe)
    else:
        X = train
    return return_run(alg, X)

def pop(dataframe, train=None):
    """ Train and predict the popularity model. """
    from Algorithms.src.algorithm.popularity import Popularity

    alg = Popularity()
    X = None
    if train == None:
        X = util.df_to_csr(dataframe)
    else:
        X = train
    return return_run(alg, X)

def iknn(dataframe, k: int = 200, normalize: bool = False, train=None):
    """ Train and predict with the Item KNN model. """
    from Algorithms.src.algorithm.item_knn import ItemKNN

    alg = ItemKNN(k=k, normalize=normalize)
    X = None
    if train == None:
        X = util.df_to_csr(dataframe)
    else:
        X = train
    return return_run(alg, X)

def trainAlgorithm(algorithmName, paramdict, dataframe, train=None):
    """ returns a dictionnary with all data """
    if algorithmName == 'wmf':
        return wmf(dataframe, float(paramdict['alpha']), int(paramdict['factors']), 
            float(paramdict['regularization']), int(paramdict['iterations']),train)

    elif algorithmName == 'ease':
        return ease(dataframe, float(paramdict['l2']),train)

    elif algorithmName == 'pop':
        return pop(dataframe,train)
        
    elif algorithmName == 'iknn':
        normalize = False
        if paramdict['normalize'] == 'true' or paramdict['normalize'] == 'True':
            normalize = True
        return iknn(dataframe, int(paramdict['k']), normalize, train)