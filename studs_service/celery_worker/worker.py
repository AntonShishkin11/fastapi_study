from celery import Celery

celery_app = Celery(
    'worker',
    broker="redis://redis:6379" #путь для докера
#    broker = 'redis:6379/0'
)



celery_app.autodiscover_tasks(["celery_worker.tasks"])

