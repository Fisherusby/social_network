## Tech Stack

- Docker Compose
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic

## Start project for the first time

```

docker-compose up -d --build
docker exec main_backend mkdir alembic/versions
docker exec main_backend alembic revision --autogenerate -m "initial table"
docker exec main_backend alembic upgrade head
```

## Stop docker-compose

```docker-compose down```

## Start created docker-compose again

```docker-compose up -d```

If have had change in db schema

```docker exec main_backend alembic upgrade head```

## Api doc (Swagger endpoint) 

[http://localhost:8080/swagger](http://localhost:8080/swagger)
