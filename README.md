setup clickupa

# Movies API - CRUD Endpoints with JWT Authentication

FastAPI application with full CRUD operations for movies, links, ratings, and tags. All endpoints are secured with JWT authentication.

## Setup

```bash
pip install -r requirements.txt
```

## Initialize Database

Create the database and default admin user:

```bash
python init_db.py
```

This creates an admin user with:
- Username: `admin`
- Password: `admin123`
- Roles: `ROLE_ADMIN`, `ROLE_USER`

## Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Running Tests

```bash
pytest -v
```

## Authentication

### JWT Token Authentication
All endpoints (except `/login`) require JWT token authentication via `Authorization: Bearer <token>` header.

### User Roles
- `ROLE_USER` - Basic user access to all CRUD endpoints
- `ROLE_ADMIN` - Admin access, required for creating new users

## API Endpoints

### Authentication Endpoints
- `POST /login` - Login with username/password, returns JWT token
- `POST /users` - Create new user (requires ROLE_ADMIN)
- `GET /user_details` - Get current user details from token

### Movies
- `GET /movies` - List all movies (requires authentication)
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

## Security Features

- **Password Hashing**: Passwords are hashed using bcrypt before storage
- **JWT Tokens**: Secure token-based authentication with 1-hour expiration
- **Role-Based Access Control**: Admin-only endpoints for user management
- **Token Verification**: All protected endpoints verify token validity and expiration

## Testing

Integration tests with fixtures are available for all endpoints:
- `test_auth.py` - 11 tests for authentication endpoints
- `test_movies.py` - 10 tests for movies endpoints
- `test_links.py` - 9 tests for links endpoints
- `test_ratings.py` - 9 tests for ratings endpoints
- `test_tags.py` - 9 tests for tags endpoints

Total: 48 integration tests covering all CRUD operations and authentication flows.

## Example Usage

### 1. Login
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Access Protected Endpoint
```bash
curl -X GET http://localhost:8000/movies \
  -H "Authorization: Bearer <your_token>"
```

### 3. Create New User (Admin Only)
```bash
curl -X POST http://localhost:8000/users \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"username": "newuser", "password": "pass123", "roles": ["ROLE_USER"]}'
```
