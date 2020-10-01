

import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, MetaData, DateTime

import os
from src import config
#import logger

# logger = logging.getLogger(__name__)
# logger.setLevel("INFO")


Base = declarative_base()



class Campaign(Base):
    """Create a data model for the Kickstarter database to be set up for capturing campaigns. """

    __tablename__ = 'kickstarter'
    id = Column(Integer, primary_key=True)
    USD_goal = Column(String(100), unique=False, nullable=False)
    staff_pick = Column(String(100), unique=False, nullable=False)
    category_name = Column(String(100), unique=False, nullable=False)
    p_category_name = Column(String(100), unique=False, nullable=False)
    blurb = Column(String(200), unique=False, nullable=False)
    name = Column(String(200), unique=False, nullable=False)
    country = Column(String(100), unique=False, nullable=False)
    num_days = Column(String(100), unique=False, nullable=False)

    def __repr__(self):
        """Creates string representation of Campaign object."""
        campaign_str = f"<Campaign ID: {self.id}, Name: {self.name}>"
        return campaign_str


def create_db(args):
    """Creates kickstarter database schema either locally or in RDS.

    Args:
        args (Argparse args): includes USD_goal, staff_pick, category_name, p_category_name, blurb, name, country, start/end dates.

    Returns:
        None
    """
    db_engine = sql.create_engine(args.engine_string)
    Base.metadata.create_all(db_engine)

    Session = sessionmaker(bind=db_engine)
    session = Session()


    campaign = Campaign(
                        name=args.name,
                        blurb=args.blurb,
                        USD_goal=args.USD_goal,
                        num_days=args.num_days,
                        country=args.country,
                        category_name=args.category_name,
                        p_category_name=args.p_category_name,
                        staff_pick=args.staff_pick
                        )

    session.add(campaign)
    session.commit()


    #logger.info("Kickstarter database created!")



def add_campaign(args):
    """
    Adds campaign object to existing RDS.

    Args:
        args (Argparse args): includes USD_goal, staff_pick, category_name, p_category_name, blurb, name, country, start/end dates.


    Returns:
        None
    """
    db_engine = sql.create_engine(args.engine_string)

    Session = sessionmaker(bind=db_engine)
    session = Session()

    campaign = Campaign(name=args.name,
                        blurb=args.blurb,
                        USD_goal=args.USD_goal,
                        num_days=args.num_days,
                        country=args.country,
                        category_name=args.category_name,
                        p_category_name=args.p_category_name,
                        staff_pick=args.staff_pick
                        )

    session.add(campaign)
    session.commit()
    session.close()
    #logger.info(f"{name} Kickstarter campaign added to database!")






