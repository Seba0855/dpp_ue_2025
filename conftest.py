import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
import models
from auth import hash_password, create_access_token


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client"""
    return TestClient(app)


@pytest.fixture
def admin_user(db):
    """Create admin user for testing"""
    user = models.User(
        username="admin",
        hashed_password=hash_password("admin123"),
        roles=["ROLE_ADMIN", "ROLE_USER"]
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def regular_user(db):
    """Create regular user for testing"""
    user = models.User(
        username="user",
        hashed_password=hash_password("user123"),
        roles=["ROLE_USER"]
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def admin_token(admin_user):
    """Generate JWT token for admin user"""
    return create_access_token(admin_user.username, admin_user.roles)


@pytest.fixture
def user_token(regular_user):
    """Generate JWT token for regular user"""
    return create_access_token(regular_user.username, regular_user.roles)


@pytest.fixture
def sample_movies(db):
    """Create sample movies for testing"""
    movies = [
        models.Movie(movieId=1, title="Toy Story (1995)", genres="Adventure|Animation|Children|Comedy|Fantasy"),
        models.Movie(movieId=2, title="Jumanji (1995)", genres="Adventure|Children|Fantasy"),
        models.Movie(movieId=3, title="Grumpier Old Men (1995)", genres="Comedy|Romance"),
    ]
    for movie in movies:
        db.add(movie)
    db.commit()
    for movie in movies:
        db.refresh(movie)
    return movies


@pytest.fixture
def sample_links(db):
    """Create sample links for testing"""
    links = [
        models.Link(movieId=1, imdbId="0114709", tmdbId="862"),
        models.Link(movieId=2, imdbId="0113497", tmdbId="8844"),
        models.Link(movieId=3, imdbId="0113228", tmdbId="15602"),
    ]
    for link in links:
        db.add(link)
    db.commit()
    for link in links:
        db.refresh(link)
    return links


@pytest.fixture
def sample_ratings(db):
    """Create sample ratings for testing"""
    ratings = [
        models.Rating(userId=1, movieId=1, rating=4.0, timestamp=964982703),
        models.Rating(userId=1, movieId=3, rating=4.0, timestamp=964981247),
        models.Rating(userId=2, movieId=1, rating=5.0, timestamp=964982224),
    ]
    for rating in ratings:
        db.add(rating)
    db.commit()
    for rating in ratings:
        db.refresh(rating)
    return ratings


@pytest.fixture
def sample_tags(db):
    """Create sample tags for testing"""
    tags = [
        models.Tag(userId=2, movieId=60756, tag="funny", timestamp=1445714994),
        models.Tag(userId=2, movieId=60756, tag="Highly quotable", timestamp=1445714996),
        models.Tag(userId=3, movieId=89774, tag="Boxing story", timestamp=1445715207),
    ]
    for tag in tags:
        db.add(tag)
    db.commit()
    for tag in tags:
        db.refresh(tag)
    return tags
