import uvicorn
from pydantic import BaseModel
from simpleeval import simple_eval
from fastapi import FastAPI

app = FastAPI()

class Expression(BaseModel):
    expr: str

@app.get("/")
async def root(): # Главная страница
    return {"mes": "Hellow World"}

@app.get("/sum/")
async def sum(a: int = 0, b: int = 0): # Сложение
    return {"sum": a+b}

@app.get("/subs/")
async def substract(a: int = 0, b: int = 0): # Вычитание
    return {"substraction": a-b}

@app.get("/mult/")
async def multiply(a: int = 0, b: int = 0): # Умножение
    return {"multiplication": a*b}

@app.post("/evaluate/")
async def evaluate_expression(expression: Expression):
    try:
        result = simple_eval(expression.expr)
        return {"expression": expression.expr, "result": result}
    except ZeroDivisionError:
        return {"error": "Division by zero"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/div/")
async def divide(a: int = 0, b: int = 0): # Деление
    return {"division": a/b}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload = True
    )