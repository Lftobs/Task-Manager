from fastapi import FastAPI, status, HTTPException
from typing import List
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String



Database_url="sqlite:///./sql_app.db"
engine = create_engine(Database_url, connect_args={"check_same_thread": False}
)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ItemDB(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

Base.metadata.create_all(bind=engine)

class Item(BaseModel):
    #id: int | None = None
    name: str
    #des:str | None = Non
    price: int
    #tax: float | None = None

class ItemList(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        orm_mode= True
    

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "hello world!"}
    
@app.post("/items/")
async def create_item(item:Item):
    session = Sessionlocal()
    items = ItemDB(name=item.name, price=item.price)
    session.add(items)
    session.commit()
    session.close()
    #session.refresh(ItemDB)
    return item

@app.get("/items/{item_id}")
async def read_items(id: int):
    session = Sessionlocal()
    items = session.query(ItemDB).get(id)
    session.close()
    if not items:
        raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
    return items

@app.get("/all", response_model= List[ItemList])
async def List_all_items():
    session = Sessionlocal()
    items_list = session.query(ItemDB).all()
    #print(items_list)
    session.close()
    return items_list

@app.put("/items/{id}")
async def update_items(id: int, newItem: Item):
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

@app.get("/item/{id}")
async def delete_item(id: int):
    session = Sessionlocal()
    item = session.query(ItemDB).get(id)
    if item:
        session.delete(item)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
    return "Item deleted"
