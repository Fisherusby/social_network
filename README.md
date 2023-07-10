## TASK

<h3>Description</h3>
Create a simple RESTful API using FastAPI for a social networking application

<h3>Functional requirements</h3>

There should be some form of authentication and registration (JWT, Oauth, Oauth 2.0, etc..)
- As a user I need to be able to signup and login
- As a user I need to be able to create, edit, delete and view posts
- As a user I can like or dislike other users’ posts but not my own 
- The API needs a UI Documentation (Swagger/ReDoc)

Completed bonus section
- Use emailhunter.co for verifying email existence on registration
- Use an in-memory DB for storing post likes and dislikes (As a cache, that gets updated whenever new likes and dislikes get added) 

## Tech Stack

- Docker Compose
- FastAPI
- PostgreSQL
- Radis
- SQLAlchemy
- Alembic

## Start project for the first time

First you rename environment file for docker-compose:
```
mv .env-dev .env
```
You can change settings in this file now or late.

After you can build and run this project:
```
docker compose up -d --build
```
And create database schema.
```
docker exec fastapi_backend mkdir alembic/versions
docker exec fastapi_backend alembic revision --autogenerate -m "initial table"
docker exec fastapi_backend alembic upgrade head
```

## UI Api Documentation (Swagger endpoint) 

[http://localhost:8080/swagger](http://localhost:8080/swagger)

## Stop docker-compose

```
docker compose down
```

## Start created docker-compose again

After completed all steps from "Start project for the first time" you can run docker-compose again without rebuild:  

```
docker compose up -d
```

If have had changes in db schema you have to run:

```
docker exec fastapi_backend alembic revision --autogenerate
docker exec fastapi_backend alembic upgrade head
```

## emailhunter.co for verifying email

If you want use emailhunter.co for verifying email you need set
EMAIL_VERIFY as True and
EMAIL_VERIFY_API_KEY as your api key from emailhunter.co platform.


