import uuid
from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_async_session
from services.stud_service import stud_service
from schemes.scheme import Student, StudentUpdate
from celery_worker.tasks import load_students_task#, delete_students_task

stud_router = APIRouter()


@stud_router.get("/get_students/", status_code=HTTPStatus.OK)
async def get_students(db: AsyncSession = Depends(get_async_session)):
    students = await stud_service.get_students(db)
    if not students:
        raise HTTPException(status_code=404, detail='Студентов в базе нет')
    return students

@stud_router.get("/get_student_by_id/", status_code=HTTPStatus.OK)
async def get_student_by_id(id: int, db: AsyncSession = Depends(get_async_session)):
    student = await stud_service.get_student_by_id(db, id)
    if not student:
        raise HTTPException(status_code=404, detail='Студент не найден')
    return student


@stud_router.get("/get_stfac/", status_code=HTTPStatus.OK)
async def get_students_by_faculty(faculty: str, db: AsyncSession = Depends(get_async_session)):
    students = await stud_service.get_students_by_faculty(db, faculty)
    if not students:
        raise HTTPException(status_code=404, detail='По этому факультету студентов не найдено')
    return students



@stud_router.get('/courses/', status_code=HTTPStatus.OK)
async def get_unique_courses(db: AsyncSession = Depends(get_async_session)):
    courses = await stud_service.get_unique_courses(db)
    if not courses:
        raise HTTPException(status_code=404, detail='Курсов не найдено')
    return courses


@stud_router.get('/average_mark/', status_code=HTTPStatus.OK)
async def get_average_mark_by_faculty(faculty: str, db: AsyncSession = Depends(get_async_session)):
    avg_mark = await stud_service.get_average_mark_by_faculty(db, faculty)
    if not avg_mark:
        raise HTTPException(status_code=404, detail='Оценок не найдено')
    return avg_mark


@stud_router.get('/lower_mark/', status_code=HTTPStatus.OK)
async def get_low_mark_students_by_course(course: str, db: AsyncSession = Depends(get_async_session)):
    low_mark = await stud_service.get_low_mark_students_by_course(db, course)
    if not low_mark:
        raise HTTPException(status_code=404, detail='Оценок не найдено')
    return low_mark

@stud_router.get('/clear_students/', status_code=HTTPStatus.OK)
async def clear_students(db: AsyncSession = Depends(get_async_session)):
    return await stud_service.clear_students(db)


@stud_router.post("/add_stud/", status_code=HTTPStatus.ACCEPTED)
async def add_stud(input: Student, db: AsyncSession = Depends(get_async_session)):
    student = await stud_service.add_stud(db, input.last_name, input.first_name, input.faculty, input.course, input.mark)
    return student


@stud_router.patch("/update_stud/", status_code=HTTPStatus.ACCEPTED)
async def update_stud(id: int, input: StudentUpdate, db: AsyncSession = Depends(get_async_session)):
    update_data = {k: v for k, v in input.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="Нет данных для обновления")
    updated_student = await stud_service.update_stud(db, id, **update_data)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return updated_student


@stud_router.delete("/del_stud/", status_code=HTTPStatus.OK)
async def del_stud(id: int, db: AsyncSession = Depends(get_async_session)):
    return await stud_service.del_stud(db, id)


@stud_router.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)

    file_path = temp_dir / f"{uuid.uuid4()}.csv"

    with open(file_path, "wb") as f_out:
        f_out.write(await file.read())

    load_students_task.delay(str(file_path))

    return {"status": "Загрузка студентов началась"}


# @stud_router.post("/delete_studs_async/")
# async def delete_students_async(ids: list[int]):
#     delete_students_task.delay(ids)
#     return {"message": f"Удаление студентов с ID: {ids}"}
