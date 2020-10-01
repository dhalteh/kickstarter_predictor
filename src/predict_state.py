
import pickle
import pandas as pd
import numpy as np
from src import config
from sklearn.ensemble import RandomForestClassifier
import logging.config

logging.config.fileConfig(config.LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger('predict_state')



def process_USD_goal(goal_entry):
    """
    Process USD_goal and checks for invalidity.

    Args:
        goal_entry (object): user entry for USD_goal

    Returns:
        goal_entry (float): processed USD goal
        invalid_flag (boolean): boolean flag for invalidity
    """
    invalid_flag = False
    try:
        goal_entry = float(goal_entry)
    except ValueError:
        invalid_flag = True
    if not invalid_flag:
        logger.debug(f"USD_goal is valid.")
    else:
        logger.warning(f"USD_goal is invalid.")
    return goal_entry, invalid_flag

def process_staff_pick(staff_pick_entry, valid_staff_picks):
    """
    Process staff_pick and checks for invalidity.

    Args:
        staff_pick_entry (object): user entry for staff_pick

    Returns:
        staff_pick_entry (object): processed user entry for staff_pick
        invalid_flag (boolean): boolean flag for invalidity
    """
    invalid_flag = False
    if not isinstance(staff_pick_entry, str):
        invalid_flag = True
    elif staff_pick_entry.lower() not in valid_staff_picks:
        invalid_flag = True
    else:
        staff_pick_entry = staff_pick_entry.lower()
        if staff_pick_entry == 'true':
            staff_pick_entry = True
        elif staff_pick_entry == 'false':
            staff_pick_entry = False

    if not invalid_flag:
        logger.debug(f"staff_pick is valid.")
    else:
        logger.warning(f"staff_pick is invalid.")
    return staff_pick_entry, invalid_flag

def get_column_levels(levels_path):
    """
    Retrieves list of levels for feature from path.

    Args:
        levels_path (string): source path containing levels .txt file.

    Returns:
        levels_list(list[string]): list of valid levels
    """
    vals = []
    try:
        with open(levels_path, 'r') as infile:
            for line in infile:
                vals.append(line.strip().lower())
        logger.debug(f"Column levels retrieved from {levels_path}")
    except:
        logger.warning("Column levels path not found!")
    return vals

def process_category(category_entry, valid_categories):
    """
    Process category entry and checks for invalidity.

    Args:
        category_entry (object): user entry for category
        valid_categories (list[string]): list of valid categories to choose from

    Returns:
        category_entry (object): processed user entry for category
        invalid_flag (boolean): boolean flag for invalidity
    """
    invalid_flag = False
    if category_entry is None:
        invalid_flag = True
    elif not isinstance(category_entry, str):
        invalid_flag = True
    elif category_entry == "":
        invalid_flag = True
    elif category_entry.lower() not in valid_categories:
        invalid_flag = True
    else:
        category_entry = category_entry.lower()

    if not invalid_flag:
        logger.debug(f"category is valid.")
    else:
        logger.warning(f"category is invalid.")
    return category_entry, invalid_flag

def process_p_category(p_category_entry, valid_p_categories):
    """
    Process parent category and checks for invalidity.

    Args:
        p_category_entry (object): user entry for parent category
        valid_p_categories (list[string]): list of valid parent categories to choose from

    Returns:
        p_category_entry (object): processed user entry for parent category
        invalid_flag (boolean): boolean flag for invalidity
    """
    invalid_flag = False
    if p_category_entry is None:
        invalid_flag = True
    elif not isinstance(p_category_entry, str):
        invalid_flag = True
    elif p_category_entry.lower() not in valid_p_categories:
        invalid_flag = True
    else:
        p_category_entry = p_category_entry.lower()

    if not invalid_flag:
        logger.debug(f"parent category is valid.")
    else:
        logger.warning(f"parent category is invalid.")
    return p_category_entry, invalid_flag

def process_blurb(blurb_entry):
    """
    Process blurb and checks for invalidity.

    Args:
        blurb_entry (object): user entry for blurb

    Returns:
        blurb_entry (object): processed user entry for blurb—if valid, returns len(blurb)
        invalid_flag (boolean): boolean flag for invalidity
    """
    invalid_flag = False
    if not isinstance(blurb_entry, str):
        invalid_flag = True
    elif blurb_entry == "":
        invalid_flag = True
    blurb_entry = len(blurb_entry.lower())

    if not invalid_flag:
        logger.debug(f"blurb is valid.")
    else:
        logger.warning(f"blurb is invalid.")
    return blurb_entry, invalid_flag

def process_name(name_entry):
    """
    Process blurb and checks for invalidity.

    Args:
        name_entry (object): user entry for name

    Returns:
        name_entry (object): processed user entry for name—if valid, returns len(name)
        invalid_flag (boolean): boolean flag for invalidity
    """
    invalid_flag = False
    if not isinstance(name_entry, str):
        invalid_flag = True
    elif name_entry == "":
        invalid_flag = True
    name_entry = len(name_entry.lower())

    if not invalid_flag:
        logger.debug(f"staff_pick is valid.")
    else:
        logger.warning(f"staff_pick is invalid.")
    return name_entry, invalid_flag

def process_country(country_entry, valid_countries):
    """
    Process country and checks for invalidity.

    Args:
        country_entry (object): user entry for name
        valid_countries (list[string]): list of valid countries to choose from

    Returns:
        country_entry (object): processed user entry for name
        invalid_flag (boolean): boolean flag for invalidity
    """
    invalid_flag = False
    if not isinstance(country_entry, str):
        invalid_flag = True
    elif country_entry.lower() not in valid_countries:
        invalid_flag = True
    else:
        country_entry = country_entry.lower()

    if not invalid_flag:
        logger.debug(f"country is valid.")
    else:
        logger.warning(f"country is invalid.")
    return country_entry, invalid_flag

def to_sec(num_days):
    """
    Converts number of days to seconds.

    Args:
        num_days (int): length of campaign in number of days

    Returns:
        num_sec (int): length of campaign in number of seconds
    """
    return num_days*24*60*60


def process_num_days(campaign_length_entry):
    """
    Process num_days, converts to seconds, and checks for invalidity.

    Args:
        campaign_length_entry (object): user entry for num_days

    Returns:
        campaign_length_entry (object): processed user entry for num_days in terms of seconds
        invalid_flag (boolean): boolean flag for invalidity
    """
    invalid_flag = False
    try:
        campaign_length_entry = to_sec(int(campaign_length_entry))
    except ValueError:
        invalid_flag = True

    if not invalid_flag:
        logger.debug(f"Number of days is valid.")
    else:
        logger.warning(f"Number of days is invalid.")
    return campaign_length_entry, invalid_flag



def make_full_dummies(data, column, all_levels):
    """
    Turns user input categorical variables into dummy variables using the full set of variable levels in the model.

    Args:
        data (Pandas DataFrame): cleaned user input dataframe
        column (string): column to convert into dummy format
        all_levels (list[string]): list of all levels for variable

    Returns:
        dummy (Pandas DataFrame): dataframe containing dummy format of desired column

    """
    dummy = pd.get_dummies(data[column]).T.reindex(all_levels).T.fillna(0)
    logger.debug("User input successfully transformed into dummy dataframe with all missing levels included.")
    return dummy

def prep_user_input(data, categorical_cols=None, numerical_cols=None, all_valid_paths=None):
    """
    Prepares user input for modeling.

    Args:
        data (Pandas DataFrame): cleaned user input dataframe
        categorical_cols (list[String]): list of categorical columns
        numerical_cols (list[String]): list of numerical columns
        all_valid_paths (list[list[string]): list of lists containing valid levels for categorical features

    """
    if categorical_cols and numerical_cols and all_valid_paths:
        dummies = []
        numerical = data[numerical_cols]
        for column, path in zip(categorical_cols, all_valid_paths):
            dummies.append(make_full_dummies(data, column, path))
        categorical = pd.concat(dummies, axis=1)
        full = pd.concat([numerical, categorical], axis=1)
        logger.debug("Data successfully prepared for model evaluation!")
        return full


def evaluate_input(model_path, prepared_input):
    """
    Evaluates prepared user input on trained model.

    Args:
        model (pickle object): path to trained random forest model pickle object
        prepared_input (Pandas DataFrame): model-ready dataframe of user input

    Returns:
        ypred (numpy array): binary state prediction for user-entered campaign info
        ypred_proba (numpy array): raw probability for state prediction
    """
    try:
        model = pickle.load(open(model_path, 'rb'))
        y_pred = model.predict(prepared_input)
        y_pred_proba = model.predict_proba(prepared_input)[:,1]
        logger.debug("User input successfully evaluated on model!")
    except:
        raise
    return y_pred, y_pred_proba


def process_user_input(user_input):
    """
    - Processes user input and checks to see if any inputted fields are invalid
    - If valid, prepares input for modeling and then evaluates on said model

    Args:
        user_input (Campaign object): user entered object of class Campaign
    """
    logger.info(f"User input-> {type(user_input)}")

    # Get column configurations
    categorical = config.CATEGORICAL
    numerical = config.NUMERICAL

    # Valid levels for categorical variables
    valid_countries = get_column_levels(config.VALID_COUNTRIES_PATH)
    valid_categories = get_column_levels(config.VALID_CATEGORIES_PATH)
    valid_p_categories = get_column_levels(config.VALID_P_CATEGORIES_PATH)
    all_valid = [valid_countries, valid_categories, valid_p_categories]



    # Check for any invalid inputs
    len_name, invalid_name = process_name(user_input.name)
    len_blurb, invalid_blurb = process_blurb(user_input.blurb)
    USD_goal, invalid_goal = process_USD_goal(user_input.USD_goal)
    time_elapsed, invalid_time = process_num_days(user_input.num_days)
    country, invalid_country = process_country(user_input.country, valid_countries=valid_countries)
    category_name, invalid_cat = process_category(user_input.category_name, valid_categories=valid_categories)
    p_category_name, invalid_pcat = process_p_category(user_input.p_category_name, valid_p_categories=valid_p_categories)
    staff_pick, invalid_staff = process_staff_pick(user_input.staff_pick, valid_staff_picks=config.VALID_STAFF_PICKS)

    # Calculate number of invalid entries
    invalid_sum = np.sum([invalid_name, invalid_blurb, invalid_goal, invalid_time, invalid_country, invalid_cat, invalid_pcat, invalid_staff])


    # If any invalid entries, return error tuple
    if invalid_sum > 0:
        logger.warning("Invalid user input! Please try again.")
        y_pred = -1
        y_pred_proba = ""
    # If entries are all valid, evaluate the input
    else:
        logger.debug("User input is valid!")
        input_dict = {
            'len_name': len_name,
            'len_blurb': len_blurb,
            'USD_goal': USD_goal,
            'time_elapsed': time_elapsed,
            'country': country,
            'category_name': category_name,
            'p_category_name': p_category_name,
            'staff_pick': staff_pick
        }
        test_data = pd.DataFrame([input_dict])

        # Prepare model input for model fitting
        model_ready_input = prep_user_input(test_data, categorical, numerical, all_valid)

        # Fit model to prepared user input
        model_path = config.MODEL_STORE_PATH

        y_pred, y_pred_proba = evaluate_input(model_path, model_ready_input)

    return y_pred, y_pred_proba







