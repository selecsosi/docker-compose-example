import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

pg_user = os.environ.get("POSTGRES_PASSWORD", "")
pg_password = os.environ.get("POSTGRES_PASSWORD", "")
pg_db = os.environ.get("POSTGRES_PASSWORD", "")
rabbit_username = os.environ.get("RABBITMQ_DEFAULT_USER", "")
rabbit_password = os.environ.get("RABBITMQ_DEFAULT_PASS", "")

backend = "redis://redis:6379"
broker = f"pyamqp://{rabbit_username}:{rabbit_password}@rabbit:5672"

app = Celery(
    'worker',
    backend=backend,
    broker=broker,
    include=['example.worker.tasks']
)

app.conf.task_routes = {'example.worker.tasks.*': {'queue': 'default'}}

if __name__ == '__main__':
    app.start()
