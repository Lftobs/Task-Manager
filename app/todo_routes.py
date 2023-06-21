from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db import Sessionlocal, engine
from app.schema import Todo_schema, todo_response, EmailSchema, todo_update
from app.model import *
from . import model
import datetime as _date
from app.mail import send_mail 

# 3rd party
from fastapi_jwt_auth import AuthJWT
#from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType


model.Base.metadata.create_all(bind=engine)

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
    return {'message': '/todos'}

@todo_r.get("/notification")
async def notification(Authorize: AuthJWT=Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token :(")

    current_user =  Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username==current_user).first()
    note = db.query(Notification).filter(Notification.user_id==User.id).all()
    return note

@todo_r.get("/all-todos", response_model= list[todo_response], status_code=200)
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
        description = todo.description,
        end_date = todo.end_date, 
        reminder = todo.reminder
    )
    new_todo.user = user
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# sort by title
@todo_r.get('/by-title')
async def get_todo_by_title(Authorize: AuthJWT=Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token :(")

    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username==current_user).first()
    print(user)
    todos = db.query(TodoDB).filter(TodoDB.user==user).order_by(TodoDB.title).all()
    
    return todos

@todo_r.get('/by-date')
async def get_todo_by_title(Authorize: AuthJWT=Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token :(")

    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username==current_user).first()
    print(user)
    todos = db.query(TodoDB).filter(TodoDB.user==user).order_by(TodoDB.end_date).all()
    
    return todos


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
async def update_todo(new: todo_update, id: int = {id}, Authorize: AuthJWT=Depends(), db: Session = Depends(get_db)):
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
    todos.description = new.description
    todos.status = new.status
    todos.end_date = new.end_date
    if todos.reminder < new.reminder:
        todos.sent_alert = False
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
    completed_todos = db.query(TodoDB).filter(TodoDB.status==Status.COMPLETED, TodoDB.user_id==user.id).all()
    
    return completed_todos

@todo_r.get("/pending-todos", status_code=200)
async def completed_todos(Authorize: AuthJWT=Depends(),  db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token :(")

    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username==current_user).first()
    pending_todos = db.query(TodoDB).filter(TodoDB.status==Status.PENDING, TodoDB.user_id==user.id).all()
    
    return pending_todos

@todo_r.get("/ip-todos", status_code=200)
async def completed_todos(Authorize: AuthJWT=Depends(),  db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token :(")

    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username==current_user).first()
    ip_todos = db.query(TodoDB).filter(TodoDB.status==Status.IN_PROGRESS, TodoDB.user_id==user.id).all()
    
    return ip_todos

# import time

# def bt(msg):
#     time.sleep(6)
#     print({'msg': msg})
#     return {'msg': msg}

# @todo_r.get('/bgt')
# async def bgt(bg: BackgroundTasks):
#     msg='hello'
#     bg.add_task(bt, msg)
#     return {'msg': 'hi'}

