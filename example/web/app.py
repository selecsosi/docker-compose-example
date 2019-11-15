import logging
from contextlib import contextmanager

from dotenv import load_dotenv
from flask import request

from .db import create_sqlalchemy_session
from .app_factory import create_app
from ..worker.tasks import do_work_async, app as celery_app

# Load environment variables if present
load_dotenv()
# Setup logging handlers if we are running through gunicorn
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app = create_app(logger_override=gunicorn_logger)
else:
    app = create_app()

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning
Session = create_sqlalchemy_session()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except BaseException as e:
        session.rollback()
        raise e
    finally:
        session.close()


@app.route('/')
def home():
    return "Hello World"


@app.route('/ping')
def ping():
    return "pong"


@app.route('/do_work')
def do_work():
    res = do_work_async()
    return f"Doing background work, taskId: {res.id}"


@app.route('/check_work')
def check_work():
    task_id = request.args.get("taskId")
    if task_id:
        res = celery_app.AsyncResult(task_id)
    else:
        return "Missing query parameter taskId"
    return f"Job Status:\n{res}"
