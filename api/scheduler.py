from rocketry import Rocketry
from rocketry.conds import every, after_success

# Creating the Rocketry app
app = Rocketry(config={"task_execution": "async"})

# Creating some tasks
@app.task(every("10 seconds"))
async def do_things():
    print("Doing a task")
    ...

@app.task(after_success(do_things))
async def do_after():
    print('next')

if __name__ == "__main__":
    # If this script is run, only Rocketry is run
    app.run()