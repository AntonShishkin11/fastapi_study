from celery import Celery

from config import REDIS_URL

celery_app = Celery(
    'worker',
    broker=REDIS_URL  # путь для докера
    #    broker = 'redis:6379/0'
)

celery_app.autodiscover_tasks(["celery_worker.tasks"])
