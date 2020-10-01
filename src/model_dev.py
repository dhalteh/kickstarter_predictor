
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, confusion_matrix, accuracy_score
import pickle
from src import config
import logging.config

logging.config.fileConfig(config.LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger('model_dev')


def make_dummies(data, categorical_cols=None):
    """
    Creates dummy columns (one-hot-encoded) for categorical variables in prep for model training.

    Args:
        data(Pandas DataFrame): data with unencoded categorical columns
        categorical_cols(List[string]): list of categorical string column names

    Returns:
        dummy_df(Pandas DataFrame): data with encoded categorical columns
    """
    dummies = []
    if categorical_cols:
        for col in categorical_cols:
            try:
                dummies.append(pd.get_dummies(data[col].str.lower()))
            except AttributeError:
                dummies.append(pd.get_dummies(data[col]))
    dummy_df = pd.concat(dummies, axis=1)
    if len(dummies) > 0:
        logger.debug("Dummy variables created!")
    else:
        logger.warning("Dummy variables are empty. Please check your configurations!")

    return dummy_df


def get_features(data_path, response, numerical=None, categorical=None):
    """
    Creates features and response datasets based on specified numerical, categorical, and response columns.
    Categorical variables are returned in one-hot-encoded formatting.

    Args:
        data_path (Pandas DataFrame): path to kickstarter data without formatted features and response
        response (string): name of response column
        numerical (List[string]): list of numerical string column names
        categorical (List[string]): list of categorical string column names

    Returns:
        df_features (Pandas DataFrame): properly formatted features dataset
        df_response (Pandas Series): properly formatted response data

    """
    if numerical and categorical:
        data = pd.read_csv(data_path)
        keep = numerical + categorical + [response]
        data = data[keep]
        numerical = data[numerical]
        categorical = make_dummies(data, categorical)
        df_features = pd.concat([numerical, categorical], axis=1)

        df_response = data[response]

        if len(df_features) != len(df_response):
            logger.warning("Feature and Response DF's are of different length! Please check before proceeding.")
        return df_features, df_response

def split_data(features, target, test_size, random_state):
    """
    Splits data into train and test datasets for training and evaluating the model.

    Args:
        features (pandas DataFrame): Complete dataset of kickstarter features
        target (pandas Series): Complete column of target values for kickstarter classification
        test_size

    Returns:
        X_train (pandas DataFrame): Complete training dataset of kickstarter features
        X_test (pandas DataFrame): Complete test dataset of kickstarter features
        y_train (pandas Series): Complete training column of target values for kickstarter classification
        y_test (pandas Series): Complete test column of target values for kickstarter classification
    """
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=test_size, random_state=random_state)
    logger.info("Data successfully split into training and test sets.")
    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train, model_path, **kwargs):
    """
    - Trains random forest classifier to predict campaign state
    - Writes pickle model object to models/logistic.pkl

    Args:
        X_train (pandas DataFrame): Complete training dataset of kickstarter features
        y_train (pandas Series): Complete training column of target values for kickstarter classification
        **kwargs (dict): Dictionary of parameters to be used by RandomForestClassifier()

    Returns:
        model (.pkl model object): Trained logistic model object
    """

    model = RandomForestClassifier(**kwargs)
    model = model.fit(X_train, y_train)

    try:
        with open(model_path, "wb") as outfile:
            pickle.dump(model, outfile)
        logger.info("Model object saved to local path.")
    except:
        logger.error("Model object not saved! Please check paths.")

    return model


def run_model(model, X_test):
    """
    Runs and scores trained model on testing data features.

    Args:
        model (.pkl model object): Trained random forest model object
        X_test (pandas DataFrame): Test dataset of kickstarter features used in model

    Returns:
        ypred_proba_test (numpy array): raw predicted probabilities array for test set
        ypred_binary_test (numpy array): binary class predictions array for test set
    """

    ypred_proba_test = model.predict_proba(X_test)[:,1]
    ypred_binary_test = model.predict(X_test)
    logger.debug("Model fitted and scored on test data.")

    return ypred_proba_test, ypred_binary_test


def evaluate_model(ypred_proba_test, ypred_binary_test, y_test, metrics_path):
    """
    Evaluates model performance on the test data using four techniques, then writes and prints results.

    Args:
        ypred_proba_test (numpy array): raw predicted probabilities array for test set
        ypred_binary_test (numpy array): binary class predictions array for test set
        y_test (numpy array): correct campaign state classification labels
        metrics_path (string): path to store model metrics

    Returns:
        auc (float): auc score
        confusion (numpy array): confusion matrix entries
        accuracy (float): test accuracy
    """

    auc = roc_auc_score(y_test, ypred_proba_test)
    confusion = confusion_matrix(y_test, ypred_binary_test)
    accuracy = accuracy_score(y_test, ypred_binary_test)

    try:
        with open(metrics_path, "w") as text_file:
            text_file.write(f"AUC: {auc} \n")
            text_file.write(f"Confusion Matrix: {confusion} \n")
            text_file.write(f"Accuracy: {accuracy} \n")
        logger.info("Model metrics successfully saved!")
    except:
        logger.warning("Model metrics not saved. Please check path!")

    print(f"AUC on test: {auc:.3f}")
    print(f"Accuracy on test: {accuracy:.3f}\n")
    print("Confusion Matrix")
    print(pd.DataFrame(confusion,
                       index=['Actual negative', 'Actual positive'],
                       columns=['Predicted negative', 'Predicted positive']))

    return auc, confusion, accuracy


def get_findings(X_train_features, model, importances_path):
    """
    Calculates and prints top 15 features and their respective importances.

    Args:
        X_train_features (list[string]): list of features used to train model
        model (.pkl model object): trained random forest model object
        importances_path (string): path to store feature importances

    Returns:
        None
    """

    feature_importances = pd.DataFrame({'feature': X_train_features,
                                        'importance': model.feature_importances_}).\
                                        sort_values('importance', ascending=False)
    print(feature_importances.head(15))
    try:
        feature_importances.to_csv(importances_path)
        logger.info("Feature importances data saved!")
    except:
        logger.warning("Feature importances not saved! Please check path.")




if __name__=="__main__":

    # Get configuration variables
    cleaned_path = config.CLEANED_STORE_PATH
    numerical = config.NUMERICAL
    categorical = config.CATEGORICAL
    response = config.RESPONSE
    split_random_state = config.SPLIT_RANDOM_STATE
    test_size = config.TEST_SIZE
    model_parameters = config.MODEL_DICT
    model_path = config.MODEL_STORE_PATH
    metrics_path = config.MODEL_METRICS_PATH
    features_path = config.MODEL_FEATURES_PATH

    # Get features and response from cleaned data
    df_features, df_response = get_features(data_path=cleaned_path, response=response, numerical=numerical, categorical=categorical)

    # Split data into training and test datasets
    X_train, X_test, y_train, y_test = split_data(features=df_features, target=df_response, test_size=test_size, random_state=split_random_state)

    # Train and save model
    model = train_model(X_train=X_train, y_train=y_train, model_path=model_path, **model_parameters)

    # Run model
    ypred_proba_test, ypred_binary_test = run_model(model=model, X_test=X_test)

    # Evaluate model
    auc, confusion, accuracy = evaluate_model(ypred_proba_test=ypred_proba_test, ypred_binary_test=ypred_binary_test, y_test=y_test, metrics_path=metrics_path)

    # Get model findings
    trained_features = [column for column in X_train.columns]
    get_findings(trained_features, model, features_path)



