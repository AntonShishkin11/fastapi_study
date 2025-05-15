import uvicorn
from fastapi import FastAPI

from api.v1.students import stud_router
from api.v1.auth import router

app = FastAPI(title="my_api")

app.include_router(stud_router, prefix="/api/v1/students")

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True
    )

# docker-compose run --rm init_db пересоздает таблицы

# docker run --name my-postgres -p 5442:5432 -e POSTGRES_PASSWORD=postgres -d postgres:latest

# Сначала включаешь в контейнерах redis и postgres
# потом командой python -m celery -A celery_worker.worker.celery_app worker --loglevel=info запускаешь celery
