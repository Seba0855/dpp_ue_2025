from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from database import engine
from auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, require_role
)

app = FastAPI()

# Create tables on startup
models.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"hello": "world"}


# ==================== AUTH ENDPOINTS ====================

@app.post("/login", response_model=schemas.Token)
def login(data: schemas.LoginData, db: Session = Depends(get_db)):
    """Login endpoint - returns JWT token"""
    user = db.query(models.User).filter(models.User.username == data.username).first()
    
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    token = create_access_token(user.username, user.roles)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("ROLE_ADMIN"))
):
    """Create new user - requires ROLE_ADMIN"""
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = models.User(
        username=user.username,
        hashed_password=hash_password(user.password),
        roles=user.roles
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user_details", response_model=schemas.UserDetails)
def get_user_details(current_user: dict = Depends(get_current_user)):
    """Get current user details from token"""
    return current_user


# ==================== MOVIES ENDPOINTS ====================

@app.get("/movies", response_model=list[schemas.Movie])
def get_movies(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    movies = db.query(models.Movie).all()
    return movies


@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def get_movie(movie_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    movie = db.query(models.Movie).filter(models.Movie.movieId == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.post("/movies", response_model=schemas.Movie, status_code=status.HTTP_201_CREATED)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_movie = db.query(models.Movie).filter(models.Movie.movieId == movie.movieId).first()
    if db_movie:
        raise HTTPException(status_code=400, detail="Movie already exists")
    
    new_movie = models.Movie(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie


@app.put("/movies/{movie_id}", response_model=schemas.Movie)
def update_movie(movie_id: int, movie: schemas.MovieUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_movie = db.query(models.Movie).filter(models.Movie.movieId == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    for key, value in movie.model_dump().items():
        setattr(db_movie, key, value)
    
    db.commit()
    db.refresh(db_movie)
    return db_movie


@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_movie = db.query(models.Movie).filter(models.Movie.movieId == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    db.delete(db_movie)
    db.commit()
    return None


# ==================== LINKS ENDPOINTS ====================

@app.get("/links", response_model=list[schemas.Link])
def get_links(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    links = db.query(models.Link).all()
    return links


@app.get("/links/{movie_id}", response_model=schemas.Link)
def get_link(movie_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    link = db.query(models.Link).filter(models.Link.movieId == movie_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


@app.post("/links", response_model=schemas.Link, status_code=status.HTTP_201_CREATED)
def create_link(link: schemas.LinkCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_link = db.query(models.Link).filter(models.Link.movieId == link.movieId).first()
    if db_link:
        raise HTTPException(status_code=400, detail="Link already exists")
    
    new_link = models.Link(**link.model_dump())
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    return new_link


@app.put("/links/{movie_id}", response_model=schemas.Link)
def update_link(movie_id: int, link: schemas.LinkUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_link = db.query(models.Link).filter(models.Link.movieId == movie_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    for key, value in link.model_dump(exclude_unset=True).items():
        setattr(db_link, key, value)
    
    db.commit()
    db.refresh(db_link)
    return db_link


@app.delete("/links/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(movie_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_link = db.query(models.Link).filter(models.Link.movieId == movie_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    db.delete(db_link)
    db.commit()
    return None


# ==================== RATINGS ENDPOINTS ====================

@app.get("/ratings", response_model=list[schemas.Rating])
def get_ratings(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    ratings = db.query(models.Rating).all()
    return ratings


@app.get("/ratings/{rating_id}", response_model=schemas.Rating)
def get_rating(rating_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    rating = db.query(models.Rating).filter(models.Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating


@app.post("/ratings", response_model=schemas.Rating, status_code=status.HTTP_201_CREATED)
def create_rating(rating: schemas.RatingCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    new_rating = models.Rating(**rating.model_dump())
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating


@app.put("/ratings/{rating_id}", response_model=schemas.Rating)
def update_rating(rating_id: int, rating: schemas.RatingUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_rating = db.query(models.Rating).filter(models.Rating.id == rating_id).first()
    if not db_rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    for key, value in rating.model_dump(exclude_unset=True).items():
        setattr(db_rating, key, value)
    
    db.commit()
    db.refresh(db_rating)
    return db_rating


@app.delete("/ratings/{rating_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(rating_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_rating = db.query(models.Rating).filter(models.Rating.id == rating_id).first()
    if not db_rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    db.delete(db_rating)
    db.commit()
    return None


# ==================== TAGS ENDPOINTS ====================

@app.get("/tags", response_model=list[schemas.Tag])
def get_tags(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tags = db.query(models.Tag).all()
    return tags


@app.get("/tags/{tag_id}", response_model=schemas.Tag)
def get_tag(tag_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@app.post("/tags", response_model=schemas.Tag, status_code=status.HTTP_201_CREATED)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    new_tag = models.Tag(**tag.model_dump())
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag


@app.put("/tags/{tag_id}", response_model=schemas.Tag)
def update_tag(tag_id: int, tag: schemas.TagUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    for key, value in tag.model_dump(exclude_unset=True).items():
        setattr(db_tag, key, value)
    
    db.commit()
    db.refresh(db_tag)
    return db_tag


@app.delete("/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    db.delete(db_tag)
    db.commit()
    return None
