from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db import Sessionlocal, engine
from app.schema import Todo_schema, todo_response, EmailSchema, todo_update
from app.model import *
import datetime as _date
from app.mail import send_mail 

# 3rd party
from fastapi_jwt_auth import AuthJWT
#from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType


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

#@scheduler.task('every 5 seconds')
#@todo_r.get("/s")
async def send_notification():
    msg = "look"
    print(msg)
#send_notification()
    # due_todos = db.query(TodoDB).filter(TodoDB.reminder>=_date.datetime.utcnow()).all()
    # for todo in due_todos:
    #     msg = f'this is to reminde you that {todo.title} ({todo.id}) has not yet been completed'
    #     send_mail(msg)
    #     new_alert = Notification(
    #         message = todo.msg,
    #         user_id = todo.user_id
    #     )
    #     new_alert.todo = todo
    #     db.add(new_alert)
    #     db.commit()
    #     db.refresh(new_alert)
    #     return new_alert
    # title = f'this is to reminde you that {todo.title} ({todo.id}) has not yet been completed'

    # new_alert = Notification(
    #     message = todo.title,
    #     user_id = todo.user_id
    # )
    # new_alert.todo = todo
    # db.add(new_alert)
    # db.commit()
    # db.refresh(new_alert)
    # return new_alert

@todo_r.get("/")
async def hello():
    return {'hi from tr'}

@todo_r.get("/n")
async def note(db: Session = Depends(get_db)):
    note = db.query(Notification).all()
    return note

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
        end_date = todo.end_date, 
        reminder = todo.reminder
    )
    new_todo.user = user
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# get todo by id endpoint
@todo_r.get("/todo/{id}", response_model= todo_response)
async def get_todo(id: int = {id}, Authorize: AuthJWT=Depends(), db: Session = Depends(get_db)):
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
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")
    
    return todos    


@todo_r.put("/update-todo/{id}", response_model= todo_response)
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
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")
    todos.title = new.title
    todos.completed = new.completed
    todos.end_date = new.end_date
    todos.reminder = new.reminder
    todos.last_updated = _date.datetime.utcnow()
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
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Todo with id {id} not found")
    if todo.user_id != user.id:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")
    db.delete(todo)
    db.commit()
    #db.refresh(todo)
    res = {
        'detail': f'Todo deleted! (Todo-id : {id}) '
    } 
    return jsonable_encoder(res)

@todo_r.get("/completed-todos", status_code=200)
async def completed_todos(Authorize: AuthJWT=Depends(),  db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token :(")

    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username==current_user).first()
    completed_todos = db.query(TodoDB).filter(TodoDB.completed==True, TodoDB.user_id==user.id).all()
    
    return completed_todos

import time

def bt(msg):
    time.sleep(6)
    print({'msg': msg})
    return {'msg': msg}

@todo_r.get('/bgt')
async def bgt(bg: BackgroundTasks):
    msg='hello'
    bg.add_task(bt, msg)
    return {'msg': 'hi'}

