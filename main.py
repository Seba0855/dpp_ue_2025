from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
from database import engine

app = FastAPI()

# Create tables on startup
models.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"hello": "world"}


@app.get("/movies")
def get_movies(db: Session = Depends(get_db)):
    movies = db.query(models.Movie).all()
    return [{"movieId": m.movieId, "title": m.title, "genres": m.genres} for m in movies]


@app.get("/links")
def get_links(db: Session = Depends(get_db)):
    links = db.query(models.Link).all()
    return [{"movieId": l.movieId, "imdbId": l.imdbId, "tmdbId": l.tmdbId} for l in links]


@app.get("/ratings")
def get_ratings(db: Session = Depends(get_db)):
    ratings = db.query(models.Rating).all()
    return [{"userId": r.userId, "movieId": r.movieId, "rating": r.rating, "timestamp": r.timestamp} for r in ratings]


@app.get("/tags")
def get_tags(db: Session = Depends(get_db)):
    tags = db.query(models.Tag).all()
    return [{"userId": t.userId, "movieId": t.movieId, "tag": t.tag, "timestamp": t.timestamp} for t in tags]
