# Task Manager - To-Do List App

Task Manager is a simple to-do list app built using FastAPI and Rocketry. It allows users to create, update, and delete tasks as well as receive notifications for their tasks. The app also includes an authentication route with user sign up and login endpoints.

Link to docs: [Task-Manager docs](https://task-manager-bvue.onrender.com/docs)

## Authentication Route
The authentication route allows users to sign up and log in to the app.

The following endpoints are available:
<!--
Sign Up
bash
Copy code
POST /signup
To create a new user account, send a POST request to the /signup endpoint with the following JSON payload:

json
Copy code
{
    "username": "your_username",
    "password": "your_password"
}
The endpoint will create a new user account with the provided username and password.

Log In
bash
Copy code
POST /login
To log in to the app, send a POST request to the /login endpoint with the following JSON payload:

json
Copy code
{
    "username": "your_username",
    "password": "your_password"
}
The endpoint will authenticate the user and return a JWT token that can be used to access the Todos route.
-->
## Todos Route
The Todos route allows users to create, update, and delete tasks as well as receive notifications for their tasks.

The following endpoints are available:
<!--
Create Task
bash
Copy code
POST /todos
To create a new task, send a POST request to the /todos endpoint with the following JSON payload:

json
Copy code
{
    "title": "your_task_title",
    "description": "your_task_description",
    "due_date": "yyyy-mm-dd"
}
The endpoint will create a new task with the provided title, description, and due date.

Update Task
bash
Copy code
PUT /todos/{task_id}
To update an existing task, send a PUT request to the /todos/{task_id} endpoint with the following JSON payload:

json
Copy code
{
    "title": "your_updated_task_title",
    "description": "your_updated_task_description",
    "due_date": "yyyy-mm-dd",
    "completed": true/false
}
The endpoint will update the task with the provided task ID and the updated task details.

Delete Task
bash
Copy code
DELETE /todos/{task_id}
To delete an existing task, send a DELETE request to the /todos/{task_id} endpoint. The endpoint will delete the task with the provided task ID.

Notification Endpoint
bash
Copy code
POST /notify
To receive notifications for tasks that are due soon, send a POST request to the /notify endpoint. The endpoint will send notifications for all tasks that are due within the next 24 hours.
-->
## Running the App Locally
To run the app locally, follow these steps:
<!--
Clone the repository to your local machine.
bash
Copy code
git clone https://github.com/your_username/task-manager.git
Navigate to the project directory.
bash
Copy code
cd task-manager
Install the project dependencies.
Copy code
pip install -r requirements.txt
Start the app.
lua
Copy code
uvicorn app.main:app --reload
The app should now be running at http://localhost:8000/.
You can now use a tool like Postman to interact with the app's endpoints.

Note: For security purposes, it is recommended to configure a secure secret key for your app and update the SECRET_KEY value in the .env file.
-->


