
import os
from pathlib import Path
import yaml


# Read in YAML file
CONFIG_SOURCE = 'config/config.yaml'
with open(CONFIG_SOURCE, "r") as infile:
    config = yaml.load(infile, Loader=yaml.FullLoader)

# Extracts parent path for this file
PARENT_PATH = Path(__file__).parent.resolve()

# Extracts root path for app repository
REPO_PATH = (PARENT_PATH / "..").resolve()

LOGGING_CONFIG = f"{REPO_PATH}/config/logging.conf"

# URL location for downloading data set
external_paths = config['source_paths']['external']
URL = external_paths['compressed_url']

# Compressed file configurations
COMPRESSED_PATH = f"{REPO_PATH}/{external_paths['compressed_path']}"

# Decompressed file configurations
NUM_SPLITS = config['acquire']['num_splits']
DECOMPRESSED_PATH = f"{REPO_PATH}/{external_paths['decompressed_path']}"

# S3 Configurations
S3_BUCKET_NAME = config['S3']['S3_bucket_name']
S3_DATA_NAME = config['S3']['S3_data_name']

# AWS Configurations
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
PORT = config['mysql']['port']
DB_NAME = config['mysql']['db_name']

# SQLITE Configurations
SQLITE_ENGINE = config['sqlite']['db_path']

# Data Path Configurations
UNCLEANED_PATH = external_paths['uncleaned_path']
CLEANED_STORE_PATH = external_paths['cleaned_path']

# Data Level Configurations
internal_paths = config['source_paths']['internal']
VALID_CATEGORIES_PATH = internal_paths['categories']
VALID_P_CATEGORIES_PATH = internal_paths['pcategories']
VALID_COUNTRIES_PATH = internal_paths['countries']
ALL_VALID_PATHS = [VALID_COUNTRIES_PATH, VALID_CATEGORIES_PATH, VALID_P_CATEGORIES_PATH]


# Model Configurations
model = config['model']
NUMERICAL = model['numerical']
CATEGORICAL = model['categorical']
RESPONSE = model['response']
VALID_STAFF_PICKS = model['staff_picks']
TEST_SIZE = model['test_size']
SPLIT_RANDOM_STATE = model['split_random_state']
MODEL_DICT = model['model_dict']

# Model Storage
model_paths = config['source_paths']['model']
MODEL_STORE_PATH = f"{REPO_PATH}/{model_paths['trained_model']}"
MODEL_METRICS_PATH = f"{REPO_PATH}/{model_paths['model_metrics']}"
MODEL_FEATURES_PATH = f"{REPO_PATH}/{model_paths['features']}"
