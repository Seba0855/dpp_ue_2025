from fastapi import FastAPI
import csv
from typing import List

app = FastAPI()


# Modele danych
class Movie:
    def __init__(self, movieId: str, title: str, genres: str):
        self.movieId = movieId
        self.title = title
        self.genres = genres


class Link:
    def __init__(self, movieId: str, imdbId: str, tmdbId: str):
        self.movieId = movieId
        self.imdbId = imdbId
        self.tmdbId = tmdbId


class Rating:
    def __init__(self, userId: str, movieId: str, rating: str, timestamp: str):
        self.userId = userId
        self.movieId = movieId
        self.rating = rating
        self.timestamp = timestamp


class Tag:
    def __init__(self, userId: str, movieId: str, tag: str, timestamp: str):
        self.userId = userId
        self.movieId = movieId
        self.tag = tag
        self.timestamp = timestamp


# Endpoint 1: Hello World
@app.get("/")
def read_root():
    return {"hello": "world"}


# Endpoint 2: Movies
@app.get("/movies")
def get_movies():
    movies = []
    with open('database/movies.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            movie = Movie(
                movieId=row['movieId'],
                title=row['title'],
                genres=row['genres']
            )
            movies.append(movie.__dict__)
    return movies


# Endpoint 3: Links
@app.get("/links")
def get_links():
    links = []
    with open('database/links.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            link = Link(
                movieId=row['movieId'],
                imdbId=row['imdbId'],
                tmdbId=row['tmdbId']
            )
            links.append(link.__dict__)
    return links


# Endpoint 4: Ratings
@app.get("/ratings")
def get_ratings():
    ratings = []
    with open('database/ratings.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            rating = Rating(
                userId=row['userId'],
                movieId=row['movieId'],
                rating=row['rating'],
                timestamp=row['timestamp']
            )
            ratings.append(rating.__dict__)
    return ratings


# Endpoint 5: Tags
@app.get("/tags")
def get_tags():
    tags = []
    with open('database/tags.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            tag = Tag(
                userId=row['userId'],
                movieId=row['movieId'],
                tag=row['tag'],
                timestamp=row['timestamp']
            )
            tags.append(tag.__dict__)
    return tags
