import asyncio
from celery import shared_task
from services import stud_service


@shared_task
def load_students_task(file_path: str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(stud_service.load_from_csv(file_path))


@shared_task
def delete_students_task(ids: list[int]):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(stud_service.delete_by_ids(ids))
