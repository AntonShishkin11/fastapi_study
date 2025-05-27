from celery import Celery
from config import REDIS_URL

broker_url = REDIS_URL
backend_url = REDIS_URL

celery_app = Celery(
    'worker',
    broker=broker_url,
    backend=backend_url,
    include=["celery_worker.tasks"]
)
#    broker = 'redis:6379/0'

celery_app.conf.update(task_track_started=True)

#docker exec -it celery_worker sh
#apt-get update && apt-get install -y iputils-ping