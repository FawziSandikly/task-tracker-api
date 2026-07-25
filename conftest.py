# Pytest configuration and fixtures for test isolation
import pytest
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_session


@pytest.fixture(name="session")
def session_fixture():
    """
    Fixture providing an in-memory SQLite session for each test.
    This ensures tests are isolated and don't affect the main database.
    """
    # Create in-memory SQLite engine with StaticPool for test thread
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Create all tables in the test database
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Fixture providing a TestClient with injected test database session.
    This allows testing endpoints with an isolated in-memory database.
    """
    def get_session_override():
        return session
    
    # Override the real database dependency with test database
    app.dependency_overrides[get_session] = get_session_override
    
    client = TestClient(app)
    yield client
    
    # Clean up dependency overrides after test
    app.dependency_overrides.clear()