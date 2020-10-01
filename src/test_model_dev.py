import pytest
import pandas as pd
from src.model_dev import *


###########################################################################################################
def test_make_dummies():
    """
    Happy path for make_dummies.
    """
    data = {
        'test1': ['a', 'b', 'c'],
        'test2': [5,6,7]
    }
    df_data = pd.DataFrame(data)
    df_test = make_dummies(df_data, ['test1'])

    true = {
        'a': [1,0,0],
        'b':[0,1,0],
        'c':[0,0,1]
    }
    df_true = pd.DataFrame(true)
    return np.isclose(df_test, df_true).all()

def test_make_dummies_unhappy():
    """
    Unhappy path for make_dummies.
    """
    data = {
        'test1': ['a', 'b', 'c'],
        'test2': [5,6,7]
    }
    df_data = pd.DataFrame(data)
    df_test = make_dummies(df_data, ['test2'])

    true = {
        '5': [1,0,0],
        '6':[0,1,0],
        '7':[0,0,1]
    }
    df_true = pd.DataFrame(true)
    return np.isclose(df_test, df_true).all()


###########################################################################################################

if __name__ == "__main__":
    test_make_dummies()
    test_make_dummies_unhappy()
