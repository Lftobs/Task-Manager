from rocketry import Rocketry
from rocketry.args import Session, Task
from app.db import Sessionlocal
from app.mail import send_mail
from app.model import TodoDB, Notification
from app.todo_routes import get_db
import datetime as _date
   
schedule = Rocketry(execution="async")

'''
still under construction 

'''

# @schedule.task('every 90 seconds')
# async def send_notification():
#     db = Sessionlocal()
#     # TODO: write logic to add new filter sent_alert=false
#     due_todos = db.query(TodoDB).filter(TodoDB.reminder<=_date.datetime.utcnow()).all()
#     for todo in due_todos:
#         msg = f'this is to reminde you that {todo.title} ({todo.id}) has not yet been completed'
#         # TODO: write logic to get user email
#         send_mail(msg)
#         # TODO: write logic to modify sent_alert=true (nb: create sent_alert column on the DB_MODELS)
#         new_alert = Notification(
#             message = msg,
#             user_id = todo.user_id
#         )
#         new_alert.todo = todo
#         db.add(new_alert)
#         db.commit()
#         db.refresh(new_alert)
        
    
#     print(due_todos)
    
# @schedule.task(execution='thread')
# def read_task(task: Task(send_notification)):
#     print(task)

# @schedule.task(execution='thread')
# def read_logs(session: Session()):
#     task = session['send_notification']
    
#     run_logs = task.logger.filter_by(action='run').all()
#     success_logs = task.logger.filter_by(action='success').all()
#     fail_logs = task.logger.filter_by(action='fail').all()

    
# if __name__ == "__main__":
#     schedule.run()