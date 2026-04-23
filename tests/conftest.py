import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, SessionLocal, get_db
from app.models import Base

@pytest.fixture(autouse=True)
def setup_db():
    # ✅ Явно создаём таблицы для тестов
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()