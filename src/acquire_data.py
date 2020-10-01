
import os
import json
import config
import boto3
import requests
import gzip
import logging.config

logging.config.fileConfig(config.LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger('acquire_data')

def get_compressed(compressed_url, compressed_path):
    """Gets compressed data set from target URL, and stores it local specified path.

    Args:
        compressed_url (string): URL location for downloading data set
        compressed_path (string): Path to store compressed data set

    Returns:
        None
    """
    response = requests.get(compressed_url)

    # Write bytes content (using 'wb' keyword)
    try:
        with open(compressed_path, 'wb') as outfile:
            outfile.write(response.content)
        logger.info('-> Compressed file successfully retrieved from URL and written to memory.')
    except:
        logger.error('-> Compressed file not retrieved! Please check URL/path configurations and try again.')
        raise(e)




def decompress_data(compressed_path, num_splits):
    """Reads in compressed json data set (json.gz), decodes and decompresses it (to .json).
     and writes file to specified path.

    Args:
        compressed_path (string): Path containing compressed (json.gz) data set
        num_splits (int): number of splits to make in data——retrieves first (most recent) of such splits

    Returns:
        decoded (list[obj]): list of .json objects
    """

    # Read in compressed json.gz, and decode
    with gzip.open(compressed_path) as decoded:
        decoded = [line.decode('utf-8') for line in decoded.readlines()]
        decoded = [json.loads(line) for line in decoded]
        subset_index = len(decoded) // num_splits
        decoded = decoded[:subset_index]
    logger.debug(f'-> Data subsetted to length: {len(decoded)}')
    logger.info(f'-> Data successfully decompressed...')

    return decoded


def write_decompressed(decompressed_data, decompressed_path):
    """
    Args:
        decompressed_data (list[obj]): list of .json objects
        decompressed_path (string): Path to store decompressed (.json) data set

    Returns:
        None
    """

    with open(decompressed_path, 'w') as outfile:
        json.dump(decompressed_data, outfile)

    logger.info(f'-> Decompressed data written to memory.')



def upload_to_S3(decompressed_path, bucket_name, data_name):
    """Uploads decompressed data set to S3 bucket according to user configurations.

    Args:
        decompressed_path (string): Path containing decompressed json data set
        bucket_name (string): Name of S3 bucket to store data set
        data_name (string): Name assigned to data set in S3

    Returns:
        None
    """
    # Establish boto3 client based on configurations
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    s3.upload_file(decompressed_path, bucket_name, data_name)
    logger.info(f'-> File successfully uploaded to S3 bucket...')


if __name__ == "__main__":


    compressed_url = config.URL
    compressed_path = config.COMPRESSED_PATH
    num_splits = config.NUM_SPLITS
    decompressed_path = config.DECOMPRESSED_PATH
    aws_access_key_id = config.AWS_ACCESS_KEY_ID
    aws_secret_access_key = config.AWS_SECRET_ACCESS_KEY
    bucket_name = config.S3_BUCKET_NAME
    data_name = config.S3_DATA_NAME

    # Get compressed
    get_compressed(compressed_url=compressed_url, compressed_path=compressed_path)

    # Decompress
    decompressed = decompress_data(compressed_path=compressed_path, num_splits=num_splits)

    # Write decompressed
    write_decompressed(decompressed_data=decompressed, decompressed_path=decompressed_path)

    # Upload data to S3 using client above
    upload_to_S3(decompressed_path=decompressed_path, bucket_name=bucket_name, data_name=data_name)



