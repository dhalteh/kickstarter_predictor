import pytest
import pandas as pd
from src.predict_state import *

###########################################################################################################


def test_process_USD_goal():
    """
    Happy test for process_USD_goal.
    """
    test = process_USD_goal(5)
    true = (5.0, False)
    assert test == true


def test_process_USD_goal_unhappy():
    """
    Unhappy test for process_USD_goal.
    """
    test = process_USD_goal("hello")
    true = ('hello', True)
    assert test == true

###########################################################################################################

def test_process_staff_pick():
    """
    Happy path for staff_pick.
    """
    test = process_staff_pick('true', ['true', 'false'])
    true = (True, False)
    assert test == true

def test_process_staff_pick_unhappy():
    """
    Unhappy path for staff_pick.
    """
    test = process_staff_pick('hello', ['true', 'false'])
    true = ('hello', True)
    assert test == true
test_process_staff_pick_unhappy()


###########################################################################################################

def test_process_category():
    """
    Happy path for process_category.
    """
    cats = ['hello', 'how', 'are', 'you']
    test = process_category('hello', cats)
    true = ('hello', False)
    assert test == true


def test_process_category_unhappy():
    """
    Unhappy path for process_category.
    """
    cats = ['hello', 'how', 'are', 'you']
    test = process_category('no', cats)
    true = ('no', True)
    assert test == true

###########################################################################################################

def test_process_p_category():
    """
    Happy path for process_p_category.
    """
    cats = ['hello', 'how', 'are', 'you']
    test = process_p_category('hello', cats)
    true = ('hello', False)
    assert test == true


def test_process_p_category_unhappy():
    """
    Unhappy path for process_p_category.
    """
    cats = ['hello', 'how', 'are', 'you']
    test = process_p_category('no', cats)
    true = ('no', True)
    assert test == true

###########################################################################################################


def test_process_blurb():
    """
    Happy path for process_blurb.
    """
    blurb = "How are you doing today?"
    test = process_blurb(blurb)
    true = (24, False)
    assert true == test

def test_process_blurb_unhappy():
    """
    Unhappy path for process_blurb.
    """
    blurb = ""
    test = process_blurb(blurb)
    true = (0, True)
    assert true == test


###########################################################################################################


def test_process_name():
    """
    Happy path for process_name.
    """
    name = "How are you doing today?"
    test = process_name(name)
    true = (24, False)
    assert true == test

def test_process_name_unhappy():
    """
    Unhappy path for process_name.
    """
    name = ""
    test = process_name(name)
    true = (0, True)
    assert true == test

###########################################################################################################

def test_process_country():
    """
    Happy path for process_country.
    """
    countries = ['us', 'au', 'mx', 'gb']
    test = process_country('au', countries)
    true = ('au', False)
    assert test == true


def test_process_country_unhappy():
    """
    Unhappy path for process_country.
    """
    countries = ['us', 'au', 'mx', 'gb']
    test = process_country('ee', countries)
    true = ('ee', True)
    assert test == true


###########################################################################################################


def test_process_num_days():
    """
    Happy test for process_num_days.
    """
    test = process_num_days(5)
    true = (432000, False)
    assert test == true


def test_process_num_days_unhappy():
    """
    Unhappy test for process_num_days.
    """
    test = process_num_days("hello")
    true = ('hello', True)
    assert test == true

###########################################################################################################


if __name__ == "__main__":
    test_process_USD_goal()
    test_process_USD_goal_unhappy()
    test_process_staff_pick()
    test_process_staff_pick_unhappy()
    test_process_category()
    test_process_category_unhappy()
    test_process_p_category()
    test_process_p_category_unhappy()
    test_process_blurb()
    test_process_blurb_unhappy()
    test_process_name()
    test_process_name_unhappy()
    test_process_country()
    test_process_country_unhappy()
    test_process_num_days()
    test_process_num_days_unhappy()