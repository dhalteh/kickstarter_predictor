
import argparse
from src.kickstarter_db import create_db, add_campaign
from datetime import datetime
from config.flaskconfig import SQLALCHEMY_DATABASE_URI


if __name__ == "__main__":

    # Add parsers to: (1) create the the Campaign db (2) add a campaign object
    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    subparsers = parser.add_subparsers()



    # Sub-parser for creating a campaign database
    sb_create = subparsers.add_parser("create_db", description="Create database")
    sb_create.add_argument("--USD_goal", default='1000', help="Goal in USD")
    sb_create.add_argument("--staff_pick", default='False', help="Is campaign featured?")
    sb_create.add_argument("--category_name", default="Food", help="Main category name")
    sb_create.add_argument("--p_category_name", default="General", help="Parent category name")
    sb_create.add_argument("--blurb", default="Blurb!", help="Campaign blurb")
    sb_create.add_argument("--name", default="Name!", help="Campaign name")
    sb_create.add_argument("--country", default="US", help="Country of origin")
    sb_create.add_argument("--num_days", default='30', help="Length of campaign in days")
    sb_create.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                            help="SQLAlchemy connection URI for database.")

    sb_create.set_defaults(func=create_db)

    # Sub-parser for ingesting new campaign data
    sb_ingest = subparsers.add_parser("add_campaign", description="Add data to database")
    sb_ingest.add_argument("--USD_goal", default='2000', help="Goal in USD")
    sb_ingest.add_argument("--staff_pick", default='False', help="Is campaign featured?")
    sb_ingest.add_argument("--category_name", default="Food", help="Main category name")
    sb_ingest.add_argument("--p_category_name", default="General", help="Parent category name")
    sb_ingest.add_argument("--blurb", default="Blurb!", help="Campaign blurb")
    sb_ingest.add_argument("--name", default="Name!", help="Campaign name")
    sb_ingest.add_argument("--country", default="US", help="Country of origin")
    sb_ingest.add_argument("--num_days", default='30', help="Length of campaign in days")
    sb_ingest.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database.")

    sb_ingest.set_defaults(func=add_campaign)

    args = parser.parse_args()
    args.func(args)