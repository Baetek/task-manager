import pytest, redis
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import (
    SQLALCHEMY_DATABASE_URL,
    TEST_SQLALCHEMY_DATABASE_URL,
    is_running_under_pytest,
    DB_RESET_ON_START,
)


if is_running_under_pytest():
    """
    This took some time,
    When running in memory sqlite requires poolclass to be StaticPool
    https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#using-a-memory-database-in-multiple-threads
    """
    engine = create_engine(
        TEST_SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
elif SQLALCHEMY_DATABASE_URL == "sqlite:///./test.db":
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else: # Prod
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )


Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

if DB_RESET_ON_START:
    Base.metadata.create_all(bind=engine)

def db_session() -> Session:
    """
    Get a database session.

    This function yields a database session and ensures it is properly closed
    after use.

    Yields
    ------
    Session
        A SQLAlchemy session to interact with the database.
    """
    db = Session()
    try:
        yield db
    finally:
        db.close()

def get_redis_client():
    try:
        client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
        client.ping()
        return client
    except (redis.ConnectionError, redis.TimeoutError):
        return None