from .config import settings
from fastapi import FastAPI, status, HTTPException
from typing import List
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import datetime as _date
import passlib.hash as _hash
from fastapi.middleware.cors import CORSMiddleware

origins = ['*']

Database_url=f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}"
engine = create_engine(Database_url)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ItemDB(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    date_added = Column(DateTime, default=_date.datetime.utcnow)

    def verify_pswd(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)

Base.metadata.create_all(bind=engine)

#schemas
class UserScheme(BaseModel):
    email: str

class UserCreate(UserScheme):
    password: str

    class Config:
        orm_mode = True

class User(UserScheme):
    id: int
    date_added: _date.datetime

    class Config:
        orm_mode = True

        

class Item(BaseModel):
    name: str
    price: int

class ItemList(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        orm_mode= True
    

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "hello world!"}
    
@app.post("/items/")
async def create_item(item:Item):
    session = Sessionlocal()
    items = ItemDB(name=item.name, price=item.price)
    session.add(items)
    session.commit()
    session.close()
    return item

@app.get("/items/{item_id}")
def read_items(id: int):
    session = Sessionlocal()
    items = session.query(ItemDB).get(id)
    session.close()
    if not items:
        raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
    return items

@app.get("/all", response_model= List[ItemList])
def List_all_items():
    session = Sessionlocal()
    items_list = session.query(ItemDB).all()
    session.close()
    return items_list

@app.put("/items/{id}")
def update_items(id: int, newItem: Item):
    session = Sessionlocal()
    item = session.query(ItemDB).get(id)
    if item:
        item.name = newItem.name
        item.price = newItem.price
        session.commit()

    session.close()
    

    if not item:
        raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
    return newItem

@app.delete("/item/{id}")
def delete_item(id: int):
    session = Sessionlocal()
    item = session.query(ItemDB).get(id)
    if item:
        session.delete(item)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
    return "Item deleted"
