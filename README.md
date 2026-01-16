setup clickupa

# Movies API - CRUD Endpoints

FastAPI application with full CRUD operations for movies, links, ratings, and tags.

## Setup

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
uvicorn main:app --reload
```

## Running Tests

```bash
pytest -v
```

## API Endpoints

### Movies
- `GET /movies` - List all movies
- `GET /movies/{movie_id}` - Get single movie
- `POST /movies` - Create new movie (returns 201)
- `PUT /movies/{movie_id}` - Update movie
- `DELETE /movies/{movie_id}` - Delete movie (returns 204)

### Links
- `GET /links` - List all links
- `GET /links/{movie_id}` - Get single link
- `POST /links` - Create new link (returns 201)
- `PUT /links/{movie_id}` - Update link
- `DELETE /links/{movie_id}` - Delete link (returns 204)

### Ratings
- `GET /ratings` - List all ratings
- `GET /ratings/{rating_id}` - Get single rating
- `POST /ratings` - Create new rating (returns 201)
- `PUT /ratings/{rating_id}` - Update rating
- `DELETE /ratings/{rating_id}` - Delete rating (returns 204)

### Tags
- `GET /tags` - List all tags
- `GET /tags/{tag_id}` - Get single tag
- `POST /tags` - Create new tag (returns 201)
- `PUT /tags/{tag_id}` - Update tag
- `DELETE /tags/{tag_id}` - Delete tag (returns 204)

## Testing

Integration tests with fixtures are available for all endpoints:
- `test_movies.py` - 9 tests for movies endpoints
- `test_links.py` - 9 tests for links endpoints
- `test_ratings.py` - 9 tests for ratings endpoints
- `test_tags.py` - 9 tests for tags endpoints

Total: 36 integration tests covering all CRUD operations.
