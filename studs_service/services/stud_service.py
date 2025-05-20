from sqlalchemy import select, func, delete, text
from sqlalchemy.ext.asyncio import AsyncSession
from cache_redis.redis_service import get_cache, set_cache, delete_cache
from config import DATABASE_URL

from database.models import Students


class StudentService():
    def __init__(self, db_url):
        self.db_url = db_url

    async def get_students(self, db: AsyncSession):
        cache_key = "students_all"
        cached = await get_cache(cache_key)
        if cached:
            return cached

        result = await db.execute(select(Students))
        students = result.scalars().all()
        data = [s.__dict__ for s in students]
        for item in data:
            item.pop('_sa_instance_state', None)
        await set_cache(cache_key, data, ex=60)
        return data

    async def get_student_by_id(self, db: AsyncSession, id):

        result = await db.execute(select(Students).where(Students.id == id))
        student = result.scalars().first()
        return student

    async def add_stud(self, db: AsyncSession, last_name, first_name, faculty, course, mark):
        student = Students(last_name=last_name, first_name=first_name, faculty=faculty, course=course, mark=mark)
        db.add(student)
        await db.commit()
        await db.refresh(student)
        await delete_cache("students_all")
        return student

    async def del_stud(self, db: AsyncSession, id):
        await db.execute(delete(Students).where(Students.id == id))
        await db.commit()
        await delete_cache("students_all")
        return {"message": f"Student with id={id} deleted"}

    async def update_stud(self, db: AsyncSession, id, **kwargs):
        stud = await db.get(Students, id)
        if not stud:
            return None

        valid_attrs = Students.__table__.columns.keys()
        for key, value in kwargs.items():
            if key in valid_attrs:
                setattr(stud, key, value)

        await db.commit()
        await db.refresh(stud)
        await delete_cache("students_all")
        return stud

    async def get_students_by_faculty(self, db: AsyncSession, faculty_name: str):
        cache_key = f"students_by_fac_{faculty_name}"
        cached = await get_cache(cache_key)
        if cached:
            return cached

        result = await db.execute(select(Students).where(Students.faculty == faculty_name))
        students = result.scalars().all()
        data = [s.__dict__ for s in students]
        for item in data:
            item.pop('_sa_instance_state', None)
        await set_cache(cache_key, data, ex=60)
        return data

    async def get_unique_courses(self, db: AsyncSession):
        cache_key = "unique_courses"
        cached = await get_cache(cache_key)
        if cached:
            return cached

        result = await db.execute(select(Students.course).distinct())
        data = result.scalars().all()
        await set_cache(cache_key, data, ex=60)
        return data

    async def get_average_mark_by_faculty(self, db: AsyncSession, faculty_name: str):
        cache_key = f"marks_by_fac_{faculty_name}"
        cached = await get_cache(cache_key)
        if cached:
            return cached

        result = await db.execute(select(func.avg(Students.mark)).where(Students.faculty == faculty_name))
        average = result.scalar()
        await set_cache(cache_key, average, ex=60)
        return round(average, 2) if average is not None else None

    async def get_low_mark_students_by_course(self, db: AsyncSession, course_name: str):
        result = await db.execute(
            select(Students).where(
                Students.course == course_name,
                Students.mark < 30
            )
        )
        students = result.scalars().all()
        data = [s.__dict__ for s in students]
        for item in data:
            item.pop('_sa_instance_state', None)
        return data

    async def clear_students(self, db: AsyncSession):
        await db.execute(text('TRUNCATE TABLE students RESTART IDENTITY CASCADE;'))
        await db.commit()
        await delete_cache("students_all")
        return {"message": "All students cleared"}


stud_service = StudentService(db_url=DATABASE_URL)
