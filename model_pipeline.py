
import numpy as np
import pandas as pd
import os
from src import config
import boto3
import botocore
import time
import ast

from src.ingest_data import read_from_S3, process_json, save_csv
from src.clean_data import read_uncleaned, make_categories, add_category_columns, make_USD_goal, make_description_vars, get_start_epoch, prep_response, save_data, write_column_levels
from src.model_dev import make_dummies, get_features, split_data, train_model, run_model, evaluate_model, get_findings

if __name__ == "__main__":

    ### Ingest Data from S3 ###

    # S3 ingest configurations
    aws_public_key = config.AWS_ACCESS_KEY_ID
    aws_private_key = config.AWS_SECRET_ACCESS_KEY
    s3_bucket_name = config.S3_BUCKET_NAME
    dataset_name = config.S3_DATA_NAME
    raw_path = config.DECOMPRESSED_PATH
    uncleaned_path = config.UNCLEANED_PATH

    # Download raw .json data from S3
    read_from_S3(aws_private_key=aws_private_key, aws_public_key=aws_public_key, s3_bucket_name=s3_bucket_name,
                 dataset_name=dataset_name, store_path=raw_path)

    # Convert to .csv
    csv_data = process_json(raw_path)

    # Save .csv to local path
    save_csv(csv_data, uncleaned_path)


    ### Clean Data ###

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


    ### Model Development ###

    # Get configuration variables
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
