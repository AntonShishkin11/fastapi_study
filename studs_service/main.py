import uvicorn
from fastapi import FastAPI

from api.v1.students import stud_router

app = FastAPI(title="my_api")

app.include_router(stud_router, prefix="/api/v1/students")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True
    )