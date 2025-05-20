from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_async_session
from services.stud_service import stud_service
from schemes.scheme import Student, StudentUpdate
from celery_worker.tasks import load_students_task, delete_students_task

stud_router = APIRouter()


@stud_router.get("/get_students/", status_code=HTTPStatus.OK)
async def get_students(db: AsyncSession = Depends(get_async_session)):
    return await stud_service.get_students(db)

@stud_router.get("/get_student_by_id/", status_code=HTTPStatus.OK)
async def get_student_by_id(id: int, db: AsyncSession = Depends(get_async_session)):
    student = await stud_service.get_student_by_id(db, id)
    if not student:
        raise HTTPException(status_code=404, detail='Студент не найден')
    return student


@stud_router.get("/get_stfac/", status_code=HTTPStatus.OK)
async def get_students_by_faculty(faculty: str, db: AsyncSession = Depends(get_async_session)):
    return await stud_service.get_students_by_faculty(db, faculty)


@stud_router.get('/courses/', status_code=HTTPStatus.OK)
async def get_unique_courses(db: AsyncSession = Depends(get_async_session)):
    return await stud_service.get_unique_courses(db)


@stud_router.get('/average_mark/', status_code=HTTPStatus.OK)
async def get_average_mark_by_faculty(faculty: str, db: AsyncSession = Depends(get_async_session)):
    return await stud_service.get_average_mark_by_faculty(db, faculty)


@stud_router.get('/lower_mark/', status_code=HTTPStatus.OK)
async def get_low_mark_students_by_course(course: str, db: AsyncSession = Depends(get_async_session)):
    return await stud_service.get_low_mark_students_by_course(db, course)


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


@stud_router.post("/load_studs/", status_code=HTTPStatus.OK)
async def load_students_async(path: str):
    load_students_task.delay(path)
    return {"message": f"Started loading students from {path}"}


@stud_router.post("/delete_studs_async/")
async def delete_students_async(ids: list[int]):
    delete_students_task.delay(ids)
    return {"message": f"Started deleting students with IDs: {ids}"}
