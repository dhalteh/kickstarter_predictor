
# Kickstarter Predictor Project Repository

### Project Owner: Daniel Halteh
### QA: Safia Khouja

- [Project Charter](#project-charter)
- [Backlog](#backlog)


## Project Charter

### I. Vision 

Kickstarter is arguably today’s most popular crowdfunding site for entrepreneurs and innovators alike, having generated nearly $5 billion total in pledges across the platform’s 180,000+ projects (as of April 2020). The website uses an “all-or-nothing” funding approach, where project owners must commit to a funding goal and deadline. If the goal is not met by the deadline, then all donated funds are returned to the original contributors. 

The vision for this project is to help any aspiring project creator gauge their likelihood of success with Kickstarter, and to ultimately help them assess whether or not Kickstarter would be an effective crowdfunding solution for their project. 


### II. Mission

The mission for this project is to create and deploy a web application that provides an interactive platform for aspiring users to determine their project’s likelihood of success—defined as meeting the funding goal by the deadline—given a set of user-entered information and characteristics pertaining to said project. 

The application’s supporting classification model will be trained on a dataset comprising of all of Kickstarter’s 180,000+ projects, and will predict a given project’s probability of success based on its features. The dataset used in the model training process was obtained through Web Robots, a large-scale web scraping and data collection website that maintains monthly datasets scraped from Kickstarter’s project pages (https://webrobots.io/kickstarter-datasets/).



### III. Success Criteria

This project will employ two metrics of success: 
- The classification model should meet an CV AUC threshold of 0.9.
- From a business-value perspective, the success of the application will be measured by comparing the success rate (in terms of attaining funding) of projects that use the application with those that do not. This difference can be shown to be statistically significant through an A/B test, which would be designed after the successful completion of the app frontend and backend.

## Backlog

### Initiative I: Model Development and Selection

**Epic I:** Develop Initial Model—In order to generate immediate business value, the goal is to develop a functional model for potential production use. This initial model can also be used as the baseline for model improvement.
- **Story 1:** Download, join, and prepare datasets (from werobots.io)<br/> 
   - Backlog: 1 point 
-	**Story 2:** Data Cleaning
      -	Address missing values
      -	Eliminate repeat observations
      -	Backlog: 2 points 
-	**Story 3:** EDA
      -	Check for completeness
      -	Look for necessary variable transformations
      -	Backlog: 2 points 
-	**Story 4:** Build simple initial model 
      -	e.g. logistic regression
      -	Goal is to get baseline for model improvement
      -	Backlog: 2 points 

**Epic II:** Model Selection and Evaluation—In terms of generating business value, implementing more complex, yet better-performing models can lead to an increase in the Cross-Validation AUC score.

-	**Story 1:** Build more complex models 
      -	Feature selection
      -	Parameter tuning
      -	e.g. boosted tree, random forest, xgboost, neural network
      -	Backlog: 4 points
-	**Story 2:** Explore additional models and methods
      -	e.g. deep learning, dimensionality reduction
      -	Icebox
-	**Story 3:** Evaluate models using CV AUC
      -	Choose optimal model based on highest resulting CV AUC score
      -	Backlog: 4 points

### Initiative II: Application Development and Cloud Infrastructure

**Epic I:** Develop Application (Frontend)—This front end interface will allow prospective Kickstarter users to use the predictor tool both quickly and efficiently. 

-	**Story 1:**  Create application using HTML/CSS and Flask
      -	Backlog: 8 points
-	**Story 2:** Create data ingestion pipeline to read-in updated Kickstarter data on a periodic basis
      -	Icebox
-	**Story 3:** Implement classification model into the web application
      -	Backlog: 8 points

**Epic II:** Cloud Setup and Deployment—Setting the application up with the proper cloud resources helps ensure the stability of the predictor tool and provides a seamless, consistent experience to the users.  

-	**Story 1:** Develop necessary cloud environment and resources (i.e. S3 buckets, RDS Instance)
      -	Backlog: 8 points
-	**Story 2:** Migrate final model and dataset to the cloud, and deploy!
      -	Backlog: 8 points
-	**Story 3:** Test application using unit and reproducibility checks
      -	Backlog: 8 points

**Epic III:** Perform an A/B Test—do users of the Kickstarter predictor have a statistically significant higher success rate for their projects compared to the general population?
 -	Icebox




## Running the Model Pipeline

### 1. Set up the Input Configurations (optional)

Navigate to the root of the app repository. If you would like to run the application the application using the default configurations, please **proceed to Step 2.**

To specify file paths (along with other desired configuration changes), please navigate to the **config.yaml** file as such:

`vi config/config.yaml`

Within this file, you can specify the source paths for the following file paths:
   
   - **decompressed_path:** path to store decompressed .json data (default = data/external/kickstarter_4_16.json)
   - **uncleaned_path:** path to store uncleaned .csv data (default = data/external/uncleaned_kickstarter.csv)
   - **cleaned_path:** path to store cleaned .csv data (default = data/external/cleaned_kickstarter.csv)
   - **categories:** path to store valid main categories (default = data/internal/main_categories.txt)
   - **pcategories:** path to store valid parent categories(default = data/internal/parent_categories.txt)
   - **countries:** path to store valid country labels (default = data/internal/countries.txt)
   - **trained_model:** path to store trained model object (default = data/models/random_forest.pkl)
   - **model_metrics:** path to store model metrics (default = data/models/model_metrics.txt)
   - **features:** path to store model feature importances (default = data/models/importances.csv)


### 2. Set up AWS and Environment Configurations

#### I: In order for the user to run the pipeline, please ensure the following:
   - Your AWS credentials must be configured as environmental variables as such:
       - `export AWS_ACCESS_KEY_ID=<your AWS access key>`
       - `export AWS_SECRET_ACCESS_KEY=<your AWS secret key>`
       
Please not that in order to pull the data from my S3 bucket, you will need to have been granted explicit access. If you do have access, you may **skip to Step 3.**

#### II. Acquire Data (if you don't have access to my S3 bucket)
To acquire the data and place it into your own S3 bucket, please configure the following **config.yaml** variables accordingly:
   - **compressed_url:** URL for desired month stamp (default = https://s3.amazonaws.com/weruns/forfun/Kickstarter/Kickstarter_2020-04-16T03_20_04_541Z.json.gz)
   - **compressed_path:** local path to store compressed .json data (default = data/external/kickstarter_4_16.json.gz)
   - **num_splits:** number of splits to make in the data—will use the most recent split (default = 10)
   - **S3_bucket_name:** < name of your S3 bucket >
   - **S3_data_name:** < name assigned to data to be stored in S3 >

With your AWS and acquisition configurations now configured, you can now download the data and upload to your own S3 bucket.

Build the data_acquisition image:

`docker build -t acquire_data .`

Run the docker container:

`docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(pwd)"/data,target=/app/data acquire_data src/acquire_data.py`

### 3.. Execute the Model Pipeline

If you have access to my S3 bucket—or if you have successfully uploaded the data to your own—you are now ready to build and run the model pipeline.

Build the model pipeline:

`docker build -t model_pipeline .`

Run the model pipeline container:

`docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(pwd)"/data,target=/app/data model_pipeline model_pipeline.py`
   

 
## Running the App 

**NOTE: Please connect to the Northwestern VPN before proceeding.**


### 1. Set up your RDS Configurations

#### SQLite (Default)

The default application configurations used SQLite to create and write a local database. If you would like to alter the input path for this database, please proceed to the **config.yaml** file.

From there, you can change **sqlite:db_path** variable as desired.

#### MYSQL (AWS)

In order to use an RDS instance on AWS through MYSQL, note the following:

This application both writes to and queries the kickstarter table. Since write access prvileges have not been granted, you will need to set up your own RDS instance and ensure that your configurations are properly pointing to that. Alternatively, you can proceed using the default SQLite set-up.

Export the **SQLALCHEMY_DATABASE_URI** as an environmental variable that points to your AWS RDS instance:

`export SQLALCHEMY_DATABASE_URI=<your RDS URI`

For reference, the SQLALCHEMY_DATABASE_URI for RDS can be formatted as such: 
   
   `{dialect}://{user}:{pw}@{host}:{port}/{db}`
   
Alternatively, you can manually specify the **SQLALCHEMY_DATABASE_URI** in the docker run command (shown in the following section).

Please note that if **SQLALCHEMY_DATABASE_URI** is NOT specified as an environmental variable, it will default to the SQLite URI specified in **config.yaml**.

### 2. Run the App

With the database URI configured, you can now build the docker image for the app:

`docker build -f app/Dockerfile -t kickstarter_app .`

Now, run the app container!

`docker run -e SQLALCHEMY_DATABASE_URI --mount type=bind,source="$(pwd)"/data,target=/app/data -p 5000:5000 --name my_app kickstarter_app`

Note: If you would like to manually set the **SQLALCHEMY_DATABASE_URI**, which will override any exisiting environmental or configuration variables, you can run the following Docker run commmand:

`docker run -e "SQLALCHEMY_DATABASE_URI={dialect}://{user}:{pw}@{host}:{port}/{db}" --mount type=bind,source="$(pwd)"/data,target=/app/data -p 5000:5000 --name my_app kickstarter_app`

### 3. Kill the Docker container

Before exiting the app, please kill the docker container as such:

`docker kill my_app`

## Testing the App 
In order to the test the app, please make sure you are back in the root directory. From there you can build the test docker image:

`docker build -t test .`

Now run the docker container to test the scripts:

`docker run test -m pytest`


## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
|   ├── internal/                     <- Internal data sources
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```


## Setting up user configurations

### 1. Set up environmental configurations

Navigate to the root of the app repository. Then access the environmental configurations file as such:

`vi src/config.env`

Edit and save the file according to your specifications for AWS and RDS. These configurations will allow you to specify the following environmental variables:

- AWS_SECRET_KEY
- USER
- PASSWORD
- HOST
- PORT
- MYSQL_DB_NAME



### 2. Set up python configurations

From the root directory, access the python configurations as such:

`vi src/config.py`

#### I. Configure your S3 variables:
 
 - S3_BUCKET_NAME (name of S3 bucket to store raw data)
 - S3_DATA_NAME (name given to file to be placed in S3)
 
#### II. Configure your AWS variables:

- AWS_PUBLIC_KEY
- AWS_SECRET_KEY

The **DB_LOCAL_FLAG** variable, when set to True (default), writes the database schema locally to SQLite. If you would like to send the schema to RDS instead, please set this flag to **False**.

This file also allows you to set paths and names for both the compressed and decompressed data sets, as desired. 



 
## Running the app in Docker

**NOTE: Please connect to the Northwestern VPN before proceeding.**

### 1. Build the Docker image

Prior to building the Docker Image, check that Docker Desktop is currently running. Given the large size of the data, please make sure to set the memory to **8GB** under **Preferences >> Resources**.

Now, build the docker image to acquire the data (using the tag kick_ingest):

`docker build -t kick_ingest .`



### 2. Run the Docker container to acquire the data

Run the the Docker container that executes the **src/acquire_data.py** script. This python script decompress the data, and stores it as a .json file in the S3 bucket corresponding to the specified configurations above.

This script will also write both the compressed and decompressed data sets locally according to the python configurations file.

`docker run --env-file=src/config.env --mount type=bind,source="$(pwd)"/data,target=/app/data kick_ingest src/acquire_data.py`



### 3. Run the Docker container to build the database

Run the Docker container that executes the **src/kickstarter_db.py** script. This python script builds the Kickstarter database schema, either locally to SQLite or on RDS/MYSQL (according to configurations file).

`docker run --env-file=src/config.env --mount type=bind,source="$(pwd)"/data,target=/app/data kick_ingest src/kickstarter_db.py`



### 4. Kill the Docker container

Before exiting the app, please kill the docker container as such:

`docker kill kick_ingest`
