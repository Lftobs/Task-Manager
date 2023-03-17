# Task Manager

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
  "password": "<your_password>",
  "email": "guy@gmail.com"
}'
```

* **Log in endpoint** 

The endpoint will authenticate the user and return a JWT token that can be used to access the Todos route.
```python
POST auth/log-in
```
    --   Request example :
```python
curl -X 'POST' \
  'https://task-manager-bvue.onrender.com/auth/log-in' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "johndoe",
  "password": "<your_password>"
}'
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
## Tools
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) ![Render](https://img.shields.io/badge/Render-%46E3B7.svg?style=for-the-badge&logo=render&logoColor=white)![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Debian](https://img.shields.io/badge/Debian-D70A53?style=for-the-badge&logo=debian&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
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
