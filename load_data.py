import csv
from database import engine, SessionLocal, Base
from models import Movie, Link, Rating, Tag


def load_movies():
    db = SessionLocal()
    try:
        with open('database/movies.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                movie = Movie(
                    movieId=int(row['movieId']),
                    title=row['title'],
                    genres=row['genres']
                )
                db.add(movie)
        db.commit()
        print("Movies loaded successfully")
    except Exception as e:
        print(f"Error loading movies: {e}")
        db.rollback()
    finally:
        db.close()


def load_links():
    db = SessionLocal()
    try:
        with open('database/links.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                link = Link(
                    movieId=int(row['movieId']),
                    imdbId=row['imdbId'],
                    tmdbId=row['tmdbId']
                )
                db.add(link)
        db.commit()
        print("Links loaded successfully")
    except Exception as e:
        print(f"Error loading links: {e}")
        db.rollback()
    finally:
        db.close()


def load_ratings():
    db = SessionLocal()
    try:
        with open('database/ratings.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                rating = Rating(
                    userId=int(row['userId']),
                    movieId=int(row['movieId']),
                    rating=float(row['rating']),
                    timestamp=int(row['timestamp'])
                )
                db.add(rating)
        db.commit()
        print("Ratings loaded successfully")
    except Exception as e:
        print(f"Error loading ratings: {e}")
        db.rollback()
    finally:
        db.close()


def load_tags():
    db = SessionLocal()
    try:
        with open('database/tags.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                tag = Tag(
                    userId=int(row['userId']),
                    movieId=int(row['movieId']),
                    tag=row['tag'],
                    timestamp=int(row['timestamp'])
                )
                db.add(tag)
        db.commit()
        print("Tags loaded successfully")
    except Exception as e:
        print(f"Error loading tags: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created")
    
    # Load data
    load_movies()
    load_links()
    load_ratings()
    load_tags()
    
    print("All data loaded successfully!")
