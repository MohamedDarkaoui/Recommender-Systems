from pathlib import Path
import random
import numpy as np
import scipy.sparse

import typer

import Algorithms.src.util as util
from Algorithms.src.algorithm.algorithm import Algorithm

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

def wmf(dataframe, alpha: float = 40.0, factors: int = 20, regularization: float = 0.01, iterations: int = 20):
    """ Train and predict with the WMF model. """
    from Algorithms.src.algorithm.wmf import WMF

    alg = WMF(alpha=alpha, num_factors=factors, regularization=regularization, iterations=iterations)
    X = util.df_to_csr(dataframe)
    return return_run(alg, X)

def ease(dataframe, l2: float = 200.0):
    """ Train and predict with the EASE model. """
    from Algorithms.src.algorithm.ease import EASE
    

    alg = EASE(l2=l2)
    X = util.df_to_csr(dataframe)
    return return_run(alg, X)

def pop(dataframe):
    """ Train and predict the popularity model. """
    from Algorithms.src.algorithm.popularity import Popularity

    alg = Popularity()
    X = util.df_to_csr(dataframe)
    return return_run(alg, X)

def iknn(dataframe, k: int = 200, normalize: bool = False):
    """ Train and predict with the Item KNN model. """
    from Algorithms.src.algorithm.item_knn import ItemKNN

    alg = ItemKNN(k=k, normalize=normalize)
    X = util.df_to_csr(dataframe)
    return return_run(alg, X)

def trainAlgorithm(algorithmName, paramdict, dataframe):
    """ returns a dictionnary with all data """
    # voor de path gan we misschien de pandas.to_csv() functie gebruiken om dat in onze directory op te slaan
    if algorithmName == 'wmf':
        return wmf(dataframe, float(paramdict['alpha']), int(paramdict['factors']), 
            float(paramdict['regularization']), int(paramdict['iterations']))

    elif algorithmName == 'ease':
        return ease(dataframe, float(paramdict['l2']))

    elif algorithmName == 'pop':
        return pop(dataframe)
        
    elif algorithmName == 'iknn':
        normalize = False
        if paramdict['normalize'] == 'true' or paramdict['normalize'] == 'True':
            normalize = True
        return iknn(dataframe, int(paramdict['k']), normalize)