from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db import Sessionlocal, engine
from . import model
from app.schema import Register, Register_res, LogIn
from app.model import User, TodoDB
#3rd party import
from fastapi_jwt_auth import AuthJWT
from werkzeug.security import generate_password_hash, check_password_hash

#TodoDB.__table__.drop(engine)
#User.__table__.drop(engine)
model.Base.metadata.create_all(bind=engine)
auth = APIRouter(
    prefix = '/auth',
    tags = ['auth']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='log-in')

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

#token: str = Depends(oauth2_scheme)

@auth.get('/')
async def hello(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required() #and Authorize._verify_jwt_in_request(token, 'access', 'headers')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token :(")
    return {'hi'}

# @auth.get('/gh')
# async def check(Authorize: AuthJWT=Depends()):
#     Authorize.jwt_required()
#     return Authorize._verify_jwt_in_request(token, 'access', 'headers')

@auth.post('/sign-up', response_model=Register_res, status_code=status.HTTP_201_CREATED)
async def Sign_up(user: Register, db: Session = Depends(get_db)):
    db_email = db.query(User).filter(User.email==user.email).first()
    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with email already exist :(")

    db_username = db.query(User).filter(User.username==user.username).first()
    if db_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with username already exist :(")
    
    new_user = User(
        username = user.username,
        email = user.email,
        password = generate_password_hash(user.password),
        is_admin = user.is_admin
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    resp = new_user
    return resp

@auth.post('/log-in', status_code=200)
async def log_in(user: LogIn, Authorize: AuthJWT=Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username==user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)

        response = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            #'token_type': 'bearer'
        }
        return jsonable_encoder(response)
    raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password :(" )

#refresh tokens
@auth.get('/refresh')
async def refresh_token(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Refresh Token :(")
    
    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=current_user)

    return jsonable_encoder({
        'access_token': access_token
    })

@auth.get('/all-todos')
async def all(db: Session = Depends(get_db)):
    #user = db.query(User).filter(User.id==13).first()
    #for u in users:
    todo = db.query(TodoDB).all()
    #db.delete(user)
    return todo #{'message': 'user deleted'}

@auth.delete('/all-users')
async def all(db: Session = Depends(get_db)):
    user = db.query(User).get(1)
    #for u in users:
    db.delete(user)
    db.commit()
    users = db.query(User).all()
    return users
