import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from app.database import db_session, engine, Base
from app.schemas import UserCreate, TaskCreate, TaskUpdate
from app.models import User, Task, TaskHistory
from app.main import create_app
from app.config import is_running_under_pytest
from alembic.config import Config
from alembic.command import upgrade, downgrade
from sqlalchemy import inspect, MetaData, Table
from alembic.script import ScriptDirectory
from alembic.runtime.environment import EnvironmentContext

@pytest.fixture(scope="module")
def alembic_config():
    config = Config("alembic.ini")
    script = ScriptDirectory.from_config(config)
    env = EnvironmentContext(config, script)
    with env:
        pass

    return config

@pytest.fixture(scope="module")
def client():
    app = create_app()
    with TestClient(app) as test_client:
        Base.metadata.create_all(bind=engine)
        yield test_client
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def session():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    Base.metadata.create_all(bind=engine)
    try:
        yield db
    finally:
        db.close()

def test_add_nickname_migration(alembic_config, session):
    upgrade(alembic_config, 'head')
    
    upgrade(alembic_config, 'e956f1ed505d')
    
    inspector = inspect(engine)
    columns = inspector.get_columns('users')
    column_names = [column['name'] for column in columns]
    assert 'nickname' in column_names

    indexes = inspector.get_indexes('users')
    index_names = [index['name'] for index in indexes]
    assert 'ix_users_nickname' in index_names

    downgrade(alembic_config, '5bcca2256ac5')

    columns = inspector.get_columns('users')
    column_names = [column['name'] for column in columns]
    assert 'nickname' not in column_names

    indexes = inspector.get_indexes('users')
    index_names = [index['name'] for index in indexes]
    assert 'ix_users_nickname' not in index_names
