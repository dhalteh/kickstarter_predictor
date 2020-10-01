
import numpy as np
import pandas as pd
import time
from src import config
import ast
import logging.config

logging.config.fileConfig(config.LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger('clean_data')


def read_uncleaned(uncleaned_path):
    """
    Reads in .csv kickstarter data as Pandas dataset.

    Args:
        uncleaned_path (string): path for .csv data.

    Returns:
        data (Pandas DataFrame): uncleaned kickstarter dataframe

    """
    try:
        data = pd.read_csv(uncleaned_path)
        logger.debug("Uncleaned data successfully read.")
    except:
        logger.error("Uncleaned data source not found!")

    return data

def make_categories(data):
    """
    Extracts category names and parent category names (if applicable) from category column.

    Args:
        data (Pandas DataFrame): Kickstarter data

    Returns:
        categories (list): list of category names to be included in new column (length => len(data)).
        parent_categories (list): list of parent category names to be included in new column (length => len(data)).

    """
    categories = []
    parent_categories = []
    for index, row in data.iterrows():
        category = ast.literal_eval(row['category'])
        try:
            categories.append(category['name'])
        except:
            categories.append('None')
        if 'parent_name' in category.keys():
            parent_categories.append(category['parent_name'])
        else:
            parent_categories.append('None')

    if (len(categories) > 0) and (len(parent_categories) > 0):
        logger.debug('Category lists successfully created.')
    else:
        logger.warning("Category lists are empty. Please check before proceeding!")
    return categories, parent_categories


def add_category_columns(data):
    """
    Adds category and parent category name columns to datset.

    Args:
        data (Pandas DataFrame): Kickstarter data.

    Returns:
        data (Pandas DataFrame): Kickstarter data with added category/parent name columns.
    """
    cat, par = make_categories(data)
    data['category_name'] = cat
    data['p_category_name'] = par
    logger.debug("Category columns created!")

    return data


def make_USD_goal(data):
    """
    Converts local currency goal to USD.

    Args:
        data (Pandas DataFrame): dataframe with campaign goals in varying currencies

    Returns:
        data (Pandas DataFrame): dataframe with campaign goals in USD
    """
    data['USD_goal'] = data['goal'] * data['static_usd_rate']
    logger.debug("USD_goal column created!")
    return data


def make_description_vars(data):
    """
    Creates description length variables for blurb and name.

    Args:
        data (Pandas DataFrame): dataframe with blurb and name vars

    Returns:
        data (Pandas DataFrame): dataframe blurb and name vars, as well as their lengths stored in new columns
    """

    data['len_blurb'] = data['blurb'].apply(lambda x: len(x))
    data['len_name'] = data['name'].apply(lambda x: len(x))
    logger.debug("Description length variables created!")

    return data


def get_start_epoch(data):

    """
    Creates time elapsed field (in terms of epochs) according to start/end dates of campaign.

    Args:
        data (Pandas DataFrame): dataframe with unformatted dates

    Returns:
        data (Pandas DataFrame): dataframe with number of epochs elapsed as new field
    """
    pattern = '%Y-%m-%d %H:%M:%S'
    data['start'] = data['created_at'].apply(lambda x: int(time.mktime(time.strptime(str(x), pattern))))
    data['time_elapsed'] = data['deadline'] - data['start']
    logger.debug("Time interval variable created!")
    return data


def prep_response(data):
    """
    Removes all entries with 'state' not resulting in either success or failure.
    Maps 'state' values to binary response.

    Args:
        data (Pandas DataFrame): dataframe with unformatted response column

    Returns:
        data (Pandas DataFrame): dataframe with formatted response column

    """
    data = data[(data['state'] == 'successful') | (data['state'] == 'failed')]
    response_dict = {'successful': 1, 'failed':0}
    data['state'] = data['state'].map(response_dict)
    logger.debug("Response variable prepared and mapped to binary output.")
    return data


def save_data(data, path):
    """
    Writes cleaned data to specified path.

    Args:
        data (Pandas DataFrame): cleaned kickstarter data
        path (string): path to store data

    Returns:
        None
    """
    try:
        data.to_csv(path)
        logger.info("Model-ready data successfully written!")
    except:
        logger.error("Cannot find path to store model-ready ready. Please check configurations!")


def write_column_levels(data, column_name, store_levels_path):
    """
    Gets unique list of valid column levels from cleaned data, and writes them to .txt file.

    Args:
        data (Pandas DataFrame): cleaned kickstarter data
        column_name (string): column from which to extract levels
        store_levels_path (string): path to store .txt file

    Returns:
        None
    """
    valid_levels = [level for level in set(data[column_name])]
    try:
        with open(store_levels_path, "w") as text_file:
            for level in valid_levels:
                text_file.write(f"{level.strip().lower()}\n")
        logger.debug("Categorical level files successfully written!")
    except:
        logger.warning("Valid categorical level files not successfully written. Please check configuration paths!")

if __name__ == "__main__":

    # Configurations
    valid_categories_path = config.VALID_CATEGORIES_PATH
    valid_p_categories_path = config.VALID_P_CATEGORIES_PATH
    valid_countries_path = config.VALID_COUNTRIES_PATH
    uncleaned_path = config.UNCLEANED_PATH
    cleaned_path = config.CLEANED_STORE_PATH

    # Read in subset data
    df = read_uncleaned(uncleaned_path=uncleaned_path)

    # Create category names
    df = add_category_columns(df)

    # Get campaign goal in USD
    df = make_USD_goal(df)

    # Get description length variables
    df = make_description_vars(df)

    # Get campaign start in epoch seconds
    df = get_start_epoch(df)

    # Prepare response variable
    df = prep_response(df)

    # Write categories to file
    write_column_levels(data=df, column_name='category_name', store_levels_path=valid_categories_path)
    write_column_levels(data=df, column_name='p_category_name', store_levels_path=valid_p_categories_path)
    write_column_levels(data=df, column_name='country', store_levels_path=valid_countries_path)


    # Save cleaned
    save_data(data=df, path=cleaned_path)










