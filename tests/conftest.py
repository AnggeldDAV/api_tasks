import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import *
from models.task import *
from db.database import Base
from main import app
from deps.deps import get_db
from core.settings import get_settings, Settings
from core import security

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_fixture():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_fixture,monkeypatch):
    def _get_db_override():
        return db_fixture
    test_settings = Settings(_env_file=".env.test")

    monkeypatch.setattr(security, "get_settings", lambda: test_settings)
    monkeypatch.setattr("deps.deps.get_settings", lambda: test_settings)

    app.dependency_overrides[get_db] = _get_db_override
    yield TestClient(app)

    app.dependency_overrides.clear()