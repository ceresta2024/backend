# Celesta RESTful API service

## Getting Started

Build and run using docker

```
docker build -t ceresta .
docker run -p 8000:8000 ceresta
```

Build and run without docker from source directory

```
pip install -r ./requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```


## Migrations

Generate an initial migration using Alembic

```
alembic revision --autogenerate -m "Create user model"
```

Apply the migration to your database
```
alembic upgrade head
```

## More

### Create env file

Create .env file in root folder, fill it with .env-example and change it according to system configuration

### Code formatter
```
black .
```
