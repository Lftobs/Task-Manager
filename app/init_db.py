from db import engine, Base
from model import *

Base.metadata.create_all(bind=engine)