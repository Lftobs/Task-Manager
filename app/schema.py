from pydantic import BaseModel
from datetime import datetime




class Register(BaseModel):
    username: str
    password: str
    email: str
    is_admin: bool | None  = False

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

class UpdateUserSchema(Register_res):
    pass

class LogIn(BaseModel):
    username: str
    password: str

# Todos schema
class Todo_schema(BaseModel):

    title: str
    completed: bool | None = False
    end_date: datetime | None = None
    reminder: datetime | None = None

    class Config:
        orm_mode=True
        schema_extra = {
            'example': {
                'title': 'Feed the chickens',
                'completed': False,
                'end_date': '2023-03-18T20:30:30.370939',
                'reminder': '2023-03-17T20:30:30.370939',
                
            }
        }
class todo_update(Todo_schema):
    #last_updated: datetime | None = None
    
    class Config:
        schema_extra = {
            'example': {
                'title': 'Feed the chickens',
                'end_date': '2023-03-18T20:30:30.370939',
                'reminder': '2023-03-17T20:30:30.370939', 
                'last_updated': '2023-03-18T20:30:30.370939',
                'completed': False
            }
        }
    
class todo_response(BaseModel):
    id: int
    title: str
    completed: bool
    end_date: datetime 
    reminder: datetime 
    last_updated: datetime
    date_added: datetime
    user_id: int

    class Config:
        orm_mode=True
        schema_extra = {
            'example': {
                'id': 2,
                'title': 'Feed the chickens',
                'completed': False,
                'end_date': '2023-03-18T20:30:30.370939',
                'reminder': '2023-03-17T20:30:30.370939', 
                'last_updated': '2023-03-18T20:30:30.370939',
                'date_added': '2023-02-18T20:30:30.370939',
                'user_id': 5
            }
        }

        
email_ls = ["papi24811@gmail.com"]

class EmailSchema(BaseModel):
    email: list[str] | None = email_ls