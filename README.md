# Task Manager - To-Do List App

Task Manager is a simple to-do list app built using FastAPI and Rocketry. It allows users to create, update, and delete tasks as well as receive notifications for their tasks. The app also includes an authentication route with user sign up and login endpoints.

**Link to docs: [Task-Manager docs](https://task-manager-bvue.onrender.com/docs)**

## Authentication Route
The authentication route allows users to sign up and log in to the app.

The following endpoints are available:

* **Sign up endpoint** 
```python
POST auth/sign-up
```
    --   Request example :
```python
curl -X 'POST' \
  'https://task-manager-bvue.onrender.com/auth/sign-up' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "guy",
  "password": "ggggycyu",
  "email": "guy@gmail.com"
}'
```

* **Log in endpoint** 

The endpoint will authenticate the user and return a JWT token that can be used to access the Todos route.
```python
POST auth/log-in
```


## Todos Route
The Todos route allows users to create, update, and delete tasks as well as receive notifications for their tasks.

The following endpoints are available:
<!--
Notification Endpoint
bash
Copy code
POST /notify
To receive notifications for tasks that are due soon, send a POST request to the /notify endpoint. The endpoint will send notifications for all tasks that are due within the next 24 hours.
-->
## Running the App Locally
To run the app locally, follow these steps:
- Clone the repository to your local machine
```console
git clone https://github.com/Lftobs/Task-Manager.git
```
- Navigate to the project directory
```console
cd Task-Manager
```
- Install the project dependencies
```console
pip install -r requirements.txt
```
- Add the necessary environment variables
- Run the application
```console
uvicorn main:app --reload
```

Note: For security purposes, it is recommended to configure a secure secret key for your app and update the SECRET_KEY value in the .env file.
