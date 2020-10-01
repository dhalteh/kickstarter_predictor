
import pytest
import pandas as pd
from src.clean_data import *

###########################################################################################################

def test_make_categories():
    """
    Happy test for make_categories.
    """
    cat1 = "{'id': 35, 'name': 'Video Games', 'slug': 'games/video games', 'position': 7, 'parent_id': 12, 'parent_name': 'Games', 'color': 51627, 'urls': {'web': {'discover': 'http://www.kickstarter.com/discover/categories/games/video%20games'}}}"
    back1 = 76
    test_dict = {
        'backers_count': back1,
        'category': cat1
    }
    test_data = pd.DataFrame([test_dict])
    true_output = (['Video Games'], ['Games'])
    assert(make_categories(test_data) == true_output)

def test_make_categories_unhappy():
    """
    Unhappy test for make_categories.
    """
    cat1 = "{'id': 35, 'slug': 'games/video games', 'position': 7, 'parent_id': 12, 'parent_name': 'Games', 'color': 51627, 'urls': {'web': {'discover': 'http://www.kickstarter.com/discover/categories/games/video%20games'}}}"
    back1 = 76
    test_dict = {
        'backers_count': back1,
        'category': cat1
    }
    test_data = pd.DataFrame([test_dict])
    true_output = ([], ['Games'])
    assert (make_categories(test_data)[0] != true_output[0])

###########################################################################################################

def test_add_category_columns():
    """
    Happy test for add_category_columns.
    """
    cat1 = "{'id': 35, 'name': 'Video Games', 'slug': 'games/video games', 'position': 7, 'parent_id': 12, 'parent_name': 'Games', 'color': 51627, 'urls': {'web': {'discover': 'http://www.kickstarter.com/discover/categories/games/video%20games'}}}"
    back1 = 76
    test_dict = {
        'backers_count': back1,
        'category': cat1,
    }
    true_dict = {
        'backers_count': back1,
        'category': cat1,
        'category_name': 'Video_Games',
        'p_category_name': 'Games'
    }
    true_output = pd.DataFrame([true_dict])
    test_data = pd.DataFrame([test_dict])
    assert(set(add_category_columns(test_data).columns) == (set(true_output.columns)))

def test_add_category_columns_unhappy():
    """
    Unhappy test for add_category_columns.
    """
    cat1 = "{'id': 35, 'slug': 'games/video games', 'position': 7, 'parent_id': 12, 'parent_name': 'Games', 'color': 51627, 'urls': {'web': {'discover': 'http://www.kickstarter.com/discover/categories/games/video%20games'}}}"
    back1 = 76
    test_dict = {
        'backers_count': back1,
        'category': cat1
    }
    test_data = pd.DataFrame([test_dict])
    true_dict = test_dict = {
        'backers_count': back1,
        'category': cat1,
        'p_category_name': 'Games'
    }
    true_df = pd.DataFrame([true_dict])
    assert len(add_category_columns(test_data).columns) != len(true_df.columns)

###########################################################################################################

def test_make_USD_goal():
    """
    Happy test for make_USD_goal.
    """
    test_dict = {
        'goal': 100,
        'static_usd_rate': 1.2,
    }
    true_dict = {
        'goal': 100,
        'static_usd_rate': 1.2,
        'USD_goal': 120.0
    }
    test_df = pd.DataFrame([test_dict])
    assert np.isclose(make_USD_goal(test_df), pd.DataFrame([true_dict])).all()



def test_make_USD_goal_unhappy():
    """
    Unhappy test for make_USD_goal.
    """
    test_dict = {
        'goal': 100,
        'static_usd_rate': np.NaN
    }
    true_dict = {
        'goal': 100,
        'static_usd_rate': 1.2,
        'USD_goal': 120.0
    }
    test_df = pd.DataFrame([test_dict])
    assert not np.isclose(make_USD_goal(test_df), pd.DataFrame([true_dict])).all()

###########################################################################################################

def test_prep_response():
    """
    Happy test for prep_response.
    """
    test_dict = {
        'state': ['successful', 'failed'],
        'test': [5,5]
    }
    test_df = pd.DataFrame(test_dict)
    test = prep_response(test_df)
    true_dict = {
        'state': [1, 0],
        'test': [5,5]
    }
    true_df = pd.DataFrame(true_dict)
    assert np.isclose(test, true_df).all()

def test_prep_response_unhappy():
    """
    Unhappy test for prep_response.
    """
    test_dict = {
        'state': ['successful', 'failed', 'live'],
        'test': [5, 5, 6]
    }
    test_df = pd.DataFrame(test_dict)
    test = prep_response(test_df)
    true_dict = {
        'state': [1, 0],
        'test': [5, 5]
    }
    true_df = pd.DataFrame(true_dict)
    assert np.isclose(test, true_df).all()


if __name__=='__main__':
    test_make_categories()
    test_make_categories_unhappy()
    test_add_category_columns()
    test_add_category_columns_unhappy()
    test_make_USD_goal()
    test_make_USD_goal_unhappy()
    test_prep_response()
    test_prep_response_unhappy()