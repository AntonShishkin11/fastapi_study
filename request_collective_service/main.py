from datetime import date
import json
import uvicorn as uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

class Appeal(BaseModel):
    last_name: str = Field(
        default='last_name',
        max_length=30
    )
    first_name: str = Field(
        default='first_name',
        max_length=30
    )
    b_date: date
    number: str = Field(
        min_length=11,
        max_length=11,
        pattern=r'^7\d{10}$')
    email: EmailStr


@app.post('/appeal')
async def appeal(model: Appeal):
    print(model.model_dump_json())  # Вывод в консоль в формате JSON
    return model.model_dump()

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True
    )