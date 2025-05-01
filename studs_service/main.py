import asyncio
import csv

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from models import Students


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

        session = self.get_async_session()


        async with session() as db:
            students = await db.execute(select(Students))
            return students.scalars().all()


    async def add_stud(self, last_name, first_name, faculty, course, mark):

        session = self.get_async_session()

        student = Students(last_name=last_name, first_name=first_name, faculty=faculty, course=course, mark=mark)

        async with session() as db:
            db.add(student)
            await db.commit()

            return student

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
        session = self.get_async_session()
        async with session() as db:
            result = await db.execute(
                select(Students).where(Students.faculty == faculty_name)
            )
            return result.scalars().all()

    async def get_unique_courses(self):
        session = self.get_async_session()
        async with session() as db:
            result = await db.execute(
                select(Students.course).distinct()
            )
            return [row[0] for row in result.all()]


    async def get_average_mark_by_faculty(self, faculty_name: str):
        session = self.get_async_session()
        async with session() as db:
            result = await db.execute(
                select(func.avg(Students.mark)).where(Students.faculty == faculty_name)
            )
            average = result.scalar()
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



async def runner():
    PG_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5442/postgres'
    stud_service = StudentService(PG_URL)


#    res = await stud_service.get_students()
#    res = await stud_service.add_stud(last_name='Alek', first_name='Johnsonss', faculty='Physics', course='Cocs', mark=323)
#    await stud_service.load_from_csv('path')

#    res = await stud_service.get_students()
#    res = await stud_service.get_students_by_faculty('ФТФ')
#    res = await stud_service.get_unique_courses()
#    res = await stud_service.get_average_mark_by_faculty('ФТФ')
    res = await stud_service.get_low_mark_students_by_course('Информатика')
    print(res)

if __name__ == '__main__':
    asyncio.run(runner())