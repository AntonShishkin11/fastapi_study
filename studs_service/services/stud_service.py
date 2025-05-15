import asyncio
import csv

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from cache_redis.redis_service import get_cache, set_cache, delete_cache

from database.models import Students

PG_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5442/postgres'


class StudentService():
    def __init__(self, db_url):
        self.db_url = db_url



    def get_async_session(self) -> AsyncSession:
        engine = create_async_engine(self.db_url)

        return sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def get_students(self):

        cache_key = "students_all"
        cached = await get_cache(cache_key)
        if cached:
            return cached

        session = self.get_async_session()

        async with session() as db:
            students = await db.execute(select(Students))
            result = students.scalars().all()
            data = [s.__dict__ for s in result]
            for item in data:
                item.pop('_sa_instance_state', None)
            await set_cache(cache_key, data, ex=60)
            return data

    async def add_stud(self, last_name, first_name, faculty, course, mark):
        session = self.get_async_session()

        student = Students(last_name=last_name, first_name=first_name, faculty=faculty, course=course, mark=mark)

        async with session() as db:
            db.add(student)
            await db.commit()
            await delete_cache("students_all")
            return student

    async def del_stud(self, id):
        session = self.get_async_session()

        async with session() as db:
            stud = await db.execute(delete(Students).where(Students.id == id))

            await db.commit()
            await delete_cache("students_all")
            return stud

    async def update_stud(self, id, **kwargs):
        session = self.get_async_session()

        async with session() as db:
            # Получаем студента по ID
            stud = await db.get(Students, id)
            if not stud:
                return None

            # Обновляем только существующие атрибуты
            valid_attrs = Students.__table__.columns.keys()
            for key, value in kwargs.items():
                if key in valid_attrs:
                    setattr(stud, key, value)

            await db.commit()
            # Обновляем объект в сессии
            await db.refresh(stud)
            await delete_cache("students_all")
            return stud

    async def load_from_csv(self, filepath):
        session = self.get_async_session()

        async with session() as db:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    last_name, first_name, faculty, course, mark = row
                    student = Students(
                        last_name=last_name.strip(),
                        first_name=first_name.strip(),
                        faculty=faculty.strip(),
                        course=course.strip(),
                        mark=int(mark.strip())
                    )
                    db.add(student)
                await db.commit()

    async def get_students_by_faculty(self, faculty_name: str):

        cache_key = "students_by_fac"
        cached = await get_cache(cache_key)
        if cached:
            return cached

        session = self.get_async_session()
        async with session() as db:
            result = await db.execute(
                select(Students).where(Students.faculty == faculty_name)
            )
            data = [s.__dict__ for s in result]
            for item in data:
                item.pop('_sa_instance_state', None)
            await set_cache(cache_key, data, ex=60)
            return result.scalars().all()

    async def get_unique_courses(self):

        cache_key = "unique_courses"
        cached = await get_cache(cache_key)
        if cached:
            return cached

        session = self.get_async_session()
        async with session() as db:
            result = await db.execute(
                select(Students.course).distinct()
            )
            data = result.scalars().all()
            await set_cache(cache_key, data, ex=60)
            return data

    async def get_average_mark_by_faculty(self, faculty_name: str):

        cache_key = "marks_by_fac"
        cached = await get_cache(cache_key)
        if cached:
            return cached

        session = self.get_async_session()
        async with session() as db:
            result = await db.execute(
                select(func.avg(Students.mark)).where(Students.faculty == faculty_name)
            )
            average = result.scalar()
            data = [s.__dict__ for s in result]
            for item in data:
                item.pop('_sa_instance_state', None)
            await set_cache(cache_key, data, ex=60)
            return round(average, 2) if average is not None else None

    async def get_low_mark_students_by_course(self, course_name: str):
        session = self.get_async_session()
        async with session() as db:
            result = await db.execute(
                select(Students).where(
                    Students.course == course_name,
                    Students.mark < 30
                )
            )
            return result.scalars().all()

    async def clear_students(self):
        session = self.get_async_session()
        async with session() as db:
            await db.execute(delete(Students))
            await db.commit()


stud_service = StudentService(PG_URL)

#    res = await stud_service.get_students()
#    res = await stud_service.add_stud(last_name='Alek', first_name='Johnsonss', faculty='Physics', course='Cocs', mark=323)
#    await stud_service.load_from_csv('path')

#    res = await stud_service.get_students()
#    res = await stud_service.get_students_by_faculty('ФТФ')
#    res = await stud_service.get_unique_courses()
#    res = await stud_service.get_average_mark_by_faculty('ФТФ')
#    res = await stud_service.get_low_mark_students_by_course('Информатика')
res = stud_service.clear_students()

if __name__ == '__main__':
    stud_service = StudentService(PG_URL)

    print(res)
