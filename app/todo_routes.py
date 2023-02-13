from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.db import Sessionlocal, engine
from app.schema import Todo_schema, todo_response
from app.model import *
# 3rd party
from fastapi_jwt_auth import AuthJWT


#model.Base.metadata.create_all(bind=engine)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

todo_r = APIRouter(
    prefix = '/todos',
    tags = ['todos']
)

@todo_r.get("/")
async def hello():
    return {'hi from tr'}

@todo_r.get("/all-todos", status_code=200)
async def all_todos(Authorize: AuthJWT=Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token :(")

    current_user =  Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username==current_user).first()
    todos = user.todos

    return todos


@todo_r.post("/create-todo", response_model= todo_response, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: Todo_schema, Authorize: AuthJWT= Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token :(")
    
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username==current_user).first()

    new_todo = TodoDB(
        title = todo.title,
    )
    new_todo.user = user
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@todo_r.put("/update-todo/{id}")
async def update_todo(new: Todo_schema, id: int = {id}, Authorize: AuthJWT=Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token :(")

    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username==current_user).first()
    todos = db.query(TodoDB).filter(TodoDB.id==id).first()
    if todos is None:
        raise HTTPException(status_code=404, detail=f"Todo with id {id} not found")
    if todos.user_id != user.id:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user id")
    todos.title = new.title
    todos.completed = new.completed
    db.commit()
    db.refresh(todos)
    return todos    

@todo_r.delete("/delete-todo/{id}")
async def delete_todo(id: int = {id}, Authorize: AuthJWT=Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token :(")

    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username==current_user).first()
    todo = db.query(TodoDB).filter(TodoDB.id==id).first()
    if todo.user_id != user.id:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user id")
    db.delete(todo)
    db.commit()
    #db.refresh(todo)
    res = {
        'detail': f'Todo deleted! (Todo-id : {id}) '
    } 
    return jsonable_encoder(res)   