from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    des:str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "hello world!"}
    
@app.post("/items/")
async def create_item(item:Item):
    return item
