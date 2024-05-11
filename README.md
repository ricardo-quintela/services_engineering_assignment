# services_engineering_assignment
<p align='center'>
    <img src="https://img.shields.io/badge/Python-gray?logo=python&logoColor=yellow" />
    <img src="https://img.shields.io/badge/Django-gray?logo=django" />
    <img src="https://img.shields.io/badge/React-gray?logo=react" />
    <img src="https://img.shields.io/badge/Typescript-gray?logo=typescript&logoColor=white" />
</p>

# Requirements

## Backend
```sh
python -m pip install requirements.txt
```

## Frontend
```sh
cd DEV/clinic_frontend
npm install
```

# Running
## Backend
```sh
cd DEV/clinic
python manage.py runserver
```

## Frontend
```sh
cd DEV/clinic_frontend
npm start
```

# Testing
## Backend
```sh
cd DEV/clinic
python manage.py test
```

## Frontend
```sh
¯\_(ツ)_/¯
```

# Architecture
The backend architecture in the cloud is as follows:

![arch](ARCH/arch.png)

## Elastic Beanstalk

Runs the django rest-framework API with the authentication system.

## Workflow

When a button is clicked, django lauches a workflow that runs a lambda function.

## S3 Buckets
Stores static files such as images for the rekognition software.

## Database

Cannot be sqlite3 (default to django). Instead SimpleDB or DynamoDB should be used. More that one should be used to separate the storage of user data and other things.
