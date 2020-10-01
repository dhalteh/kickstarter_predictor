
import numpy as np
import pandas as pd
import os
from src import config
import boto3
import botocore
import logging.config

logging.config.fileConfig(config.LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger('ingest_data')

# Ingests raw, uncleaned data from S3

def read_from_S3(aws_public_key, aws_private_key, s3_bucket_name, dataset_name, store_path):
    """
    Pulls in raw, decompressed .json kickstarter data from S3 bucket.

    Args:
        aws_public_key (string): public key variable to access S3
        aws_private_key (string): private key variable to access S3
        s3_bucket_name (string): name of S3 bucket containing desired dataset
        dataset_name (string): name of desired dataset
        store_path (string): local path to store raw data from S3

    Returns:
        None.
    """
    # Establish S3 connection
    try:
        s3 = boto3.resource("s3", aws_access_key_id=aws_public_key, aws_secret_access_key=aws_private_key)
        logging.debug('S3 connection successfully extablished')
    except:
        logging.error("Could not establish connection to S3 bucket. Please check your configurations and try again!")


    # Pull in the data and store in store_path
    try:
        bucket = s3.Bucket(s3_bucket_name)
        bucket.download_file(dataset_name, store_path)
        logging.info("Data successfully pulled from S3 bucket.")
    except:
        logging.error("Could not download dataset. Please check both the file name and store path!")



def process_json(path):
    """
    Reads in .json dataset from path, extracts Kickstarter data, and converts to Pandas DataFrame.

    Args:
        path (string): path for retrieving master .json dataset.

    Returns:
        df (Pandas DataFrame): subsetted dataframe containing relevant Kickstarter data
    """
    try:
        df = pd.read_json(path)
        df = pd.read_json(df['data'].to_json(), orient='index')
        logging.debug(f".json data successfully converted Pandas DataFrame.")
    except:
        logging.error("Unable to convert .json file. Please check formatting.")

    return df

def save_csv(df, store_path):
    """
    Writes uncleaned subset .csv file to local path.

    Args:
        df (Pandas DataFrame): subsetted dataframe containing relevant Kickstarter data
        store_path (string): path for storing uncleaned subsetted data

    Returns:
        None
    """
    try:
        df.to_csv(store_path)
        logging.info(f"Uncleaned data of length {len(df)} saved to local path.")
    except:
        logging.error("Unable to save uncleaned data.")



if __name__ == "__main__":

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
    
    

