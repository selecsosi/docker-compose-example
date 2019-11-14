import os
from contextlib import contextmanager
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, request, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..worker.tasks import do_work_async


load_dotenv()
app = Flask("web")
pg_user = os.environ.get("POSTGRES_PASSWORD", "")
pg_password = os.environ.get("POSTGRES_PASSWORD", "")
pg_db = os.environ.get("POSTGRES_PASSWORD", "")
connection_string = f'postgresql+psycopg2://{pg_user}:{pg_password}@postgres/{pg_db}'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

engine = create_engine(connection_string, pool_pre_ping=True)
# configure Session class with desired options
Session = sessionmaker()
# associate it with our custom Session class
Session.configure(bind=engine)

api_key, api_secret = "username:password".split(":")


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    if api_key is not None:
        return username == api_key and password == api_secret
    else:
        return True


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        '{"message": "Could not verify your access level for that URL. You have to login with proper credentials"}',
        401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


@app.route('/ping')
def ping():
    return "pong"


@app.route('/do_work')
def do_work():
    res = do_work_async()
    return f"Doing background work, job id: {res.id}"
