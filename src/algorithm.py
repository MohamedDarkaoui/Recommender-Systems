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

def return_run(alg: Algorithm, X: scipy.sparse.csr_matrix, top_k: int = 5):
    """ Train a model and show the recommendations for random users. """
    random.seed(SEED)
    np.random.seed(SEED)

    alg.fit(X)
    return get_recommendations(alg, X, top_k=top_k)

def get_recommendations(alg: Algorithm, X: scipy.sparse.csr_matrix, top_k: int = 5):
    """ Show the recommendations for random users. """
    random.seed(SEED)
    np.random.seed(SEED)

    test_users = random.sample(list(range(X.shape[0])), AMOUNT_TEST_USERS)
    test_histories = X[test_users, :]
    predictions = alg.predict(test_histories)
    recommendations, scores = util.predictions_to_recommendations(predictions, top_k=top_k)
    return_dict = {'users':[],'history':[],'recommendations':[],'scores':[]}
    for index, u in enumerate(test_users):
        return_dict['users'].append(u)
        return_dict['history'].append(np.where(test_histories[index].toarray().flatten())[0])
        return_dict['recommendations'].append(recommendations[index])
        return_dict['scores'].append(scores[index])
    
    return return_dict


def wmf(path: Path = PathArgument, item_col: str = "movieId", user_col: str = "userId", top_k: int = 5,
         alpha: float = 40.0, factors: int = 20, regularization: float = 0.01, iterations: int = 20):
    """ Train and predict with the WMF model. """
    from Algorithms.src.algorithm.wmf import WMF

    alg = WMF(alpha=alpha, num_factors=factors, regularization=regularization, iterations=iterations)
    X = util.path_to_csr(path, item_col=item_col, user_col=user_col)
    return return_run(alg, X, top_k=top_k)

def ease(path: Path = PathArgument, item_col: str = "movieId", user_col: str = "userId", top_k: int = 5,
         l2: float = 200.0):
    """ Train and predict with the EASE model. """
    from Algorithms.src.algorithm.ease import EASE

    alg = EASE(l2=l2)
    X = util.path_to_csr(path, item_col=item_col, user_col=user_col)
    return return_run(alg, X, top_k=top_k)

def pop(path: Path = PathArgument, item_col: str = "movieId", user_col: str = "userId", top_k: int = 5):
    """ Train and predict the popularity model. """
    from Algorithms.src.algorithm.popularity import Popularity

    alg = Popularity()
    X = util.path_to_csr(path, item_col=item_col, user_col=user_col)
    return return_run(alg, X, top_k=top_k)

def iknn(path: Path = PathArgument, item_col: str = "movieId", user_col: str = "userId", top_k: int = 5,
         k: int = 200, normalize: bool = False):
    """ Train and predict with the Item KNN model. """
    from Algorithms.src.algorithm.item_knn import ItemKNN

    alg = ItemKNN(k=k, normalize=normalize)
    X = util.path_to_csr(path, item_col=item_col, user_col=user_col)
    return return_run(alg, X, top_k=top_k)

def runAlgorithm(algorithmName, paramdict, file_path):
    """ returns a dictionnary with all data """
    # voor de path gan we misschien de pandas.to_csv() functie gebruiken om dat in onze directory op te slaan
    if algorithmName == 'wmf':
        return wmf(file_path,'movieId','userId', int(paramdict['top_k_wmf']),
        float(paramdict['alpha']),int(paramdict['factors']),float(paramdict['regularization']), int(paramdict['iterations']))
    elif algorithmName == 'ease':
        return ease(file_path,'movieId','userId', int(paramdict['top_k_ease']),float(paramdict['l2']))
    elif algorithmName == 'pop':
        return pop(file_path,'movieId','userId',int(paramdict['top_k_pop']))
    elif algorithmName == 'iknn':
        normalize = False
        if paramdict['normalize'] == 'true' or paramdict['normalize'] == 'true':
            normalize = True
        return iknn(file_path,'movieId','userId',int(paramdict['top_k_iknn']),int(paramdict['k']),normalize)