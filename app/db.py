from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings


Database_url=f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}"
#Database_url = 'postgresql://lf_db_user:2xrvorbyf7nsF0HEk3ZFc5oOxddkgxWO@dpg-ceksc61gp3jlcslvr9h0-a.oregon-postgres.render.com/lf_db'
engine = create_engine(Database_url, echo=True)

Base = declarative_base()

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = Sessionlocal()