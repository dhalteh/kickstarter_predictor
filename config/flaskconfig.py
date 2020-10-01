
import os
import yaml

# Read in YAML file
CONFIG_SOURCE = 'config/config.yaml'
with open(CONFIG_SOURCE, "r") as infile:
    config = yaml.load(infile, Loader=yaml.FullLoader)

print(config['sqlite']['db_path'])

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 5000
APP_NAME = "kickstarter_predictor"
HOST = "0.0.0.0"


# # MYSQL Configurations
# MYSQL_USER = os.environ.get('MYSQL_USER')
# MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
# MYSQL_HOST = os.environ.get('MYSQL_HOST')
# MYSQL_PORT = os.environ.get('MYSQL_PORT')
# MYSQL_DATABASE = os.environ.get('MYSQL_DB_NAME')
# CONN_TYPE = "mysql+pymysql"
# MYSQL_ENGINE = "{}://{}:{}@{}:{}/{}".format(CONN_TYPE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE)

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
print(SQLALCHEMY_DATABASE_URI)
if SQLALCHEMY_DATABASE_URI is None:
    SQLALCHEMY_DATABASE_URI = config['sqlite']['db_path']
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100

