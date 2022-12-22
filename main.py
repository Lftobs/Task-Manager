from fastapi import FastAPI, Path
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    des:str | None = None
    price: float
    tax: float | None = None

class User(BaseModel):
    name: str
    age: int
    nick_name: str

app = FastAPI()

@app.get("/")
async def home():
    return {"mes": "hi"}
    
@app.post("/items/")
async def create_item(item:Item):
    return item

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/tobs/{fn}")
async def name(fn: int):
    return {"firstname": fn}

@app.put("/tobs/{fn}")
async def name(fn: int, q: str | None = None, item: Item | None = None):
    results = {"item_id": fn}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

@app.post("/prat/")
async def user(user: User):
    return user
