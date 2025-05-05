from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from database.models import Students
from database.stud_service import stud_service
from schemes.scheme import Student, StudentUpdate

stud_router = APIRouter()

@stud_router.get("/get_students/", status_code=HTTPStatus.OK)
async def get_students():
    return await stud_service.get_students()

@stud_router.post("/add_stud/", status_code=HTTPStatus.ACCEPTED)
async def add_stud(input: Student):
    student = await stud_service.add_stud(input.last_name, input.first_name, input.faculty, input.course, input.mark)
    return student

@stud_router.patch("update_stud", status_code=HTTPStatus. ACCEPTED)
async def update_stud(id: int, input: StudentUpdate):
    # Словарь только с переданными (не None) полями
    update_data = {k: v for k, v in input.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="Нет данных для обновления")
    updated_student = await stud_service.update_stud(id, **update_data)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return updated_student

@stud_router.delete("/del_stud/", status_code=HTTPStatus.OK)
async def del_stud(id: int):
    return await stud_service.del_stud(id)