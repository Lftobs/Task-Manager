from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth
from app.todo_routes import todo_r
from app.config import Settings
import asyncio
import uvicorn
import logging
from app.scheduler import schedule


# 3rd party
from fastapi_jwt_auth import AuthJWT

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(auth)
app.include_router(todo_r)


@app.on_event('startup')
async def on_startup():
    logger = logging.getLogger('rocketry.task')
    logger.addHandler(logging.StreamHandler())
    asyncio.create_task(schedule.serve())


@app.on_event('shutdown')
def on_shutdown():
    print('shutdown')
    schedule.session.shut_down()

'''
class Server(uvicorn.Server):
    def handle_exit(self, sig: int, frame) -> None:
        schedule.session.shut_down()
        return super().handle_exit(sig, frame)
    
async def main():
    server = Server(config=uvicorn.Config(app, workers=1, loop="asyncio"))
    api = asyncio.create_task(server.serve())
    sched = asyncio.create_task(schedule.serve())
    
    await asyncio.wait([sched, api])
    
if __name__ =="__main__":
    
    # print rocketry's logs to terminal 
    logger = logging.getLogger('rocketry.task')
    print('hi')
    logger.addHandler(logging.StreamHandler())
    #run both app(rocketry & fastapi)
    asyncio.run(main())    
'''
