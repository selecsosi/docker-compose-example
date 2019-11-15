import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_sqlalchemy_session():
    pg_user = os.environ.get("POSTGRES_PASSWORD")
    pg_password = os.environ.get("POSTGRES_PASSWORD")
    pg_db = os.environ.get("POSTGRES_PASSWORD")
    connection_string = f'postgresql+psycopg2://{pg_user}:{pg_password}@postgres/{pg_db}'
    engine = create_engine(connection_string, pool_pre_ping=True)
    # configure Session class with desired options
    session = sessionmaker()
    # associate it with our custom Session class
    session.configure(bind=engine)
    return session
