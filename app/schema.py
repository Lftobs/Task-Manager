from pydantic import BaseModel
from datetime import datetime

# username = Column(String(30), unique=True)
#     password = Column(Text, nullable=True)
#     email = Column(String, unique=True)
#     is_admin = Column(Boolean, default=False)


class Register(BaseModel):
    username: str
    password: str
    email: str
    #is_admin: bool

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'username': 'guy',
                'password': 'password',
                'email': 'guy@gmail.com',
                #'is_admin': False
            }
        }
    
class Register_res(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


class LogIn(BaseModel):
    username: str
    password: str

# Todos schema
class Todo_schema(BaseModel):

    title: str
    completed: bool | None = False

    class Config:
        orm_mode=True
        schema_extra = {
            'example': {
                'title': 'Feed the chickens',
                'completed': False
            }
        }

class todo_response(BaseModel):
    id: int
    title: str
    completed: bool
    date_added: datetime
    user_id: int

    class Config:
        orm_mode=True
        schema_extra = {
            'example': {
                'id': 2,
                'title': 'Feed the chickens',
                'completed': False,
                'datetime': '2008:34:67 19:34',
                'user_id': 5
            }
        }