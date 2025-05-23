import asyncio
import os

from celery import shared_task

from database.session import async_session
from services.stud_service import StudentService


@shared_task
def load_students_task(file_path: str):

    async def run():
        async with async_session() as db:
            await StudentService.load_from_csv(db, file_path)

    try:
        asyncio.run(run())
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

# @shared_task
# def delete_students_task(ids: list[int]):
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(StudentService.delete_by_ids(ids))
