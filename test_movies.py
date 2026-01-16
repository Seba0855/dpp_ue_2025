import pytest
from fastapi import status


class TestMoviesEndpoints:
    """Integration tests for Movies CRUD endpoints"""

    def test_get_movies_list(self, client, sample_movies, admin_token):
        """Test GET /movies returns all movies from fixtures"""
        response = client.get(
            "/movies",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        assert data[0]["movieId"] == 1
        assert data[0]["title"] == "Toy Story (1995)"
        assert "Adventure" in data[0]["genres"]

    def test_get_movies_without_token(self, client, sample_movies):
        """Test GET /movies without authentication token"""
        response = client.get("/movies")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_movie_by_id(self, client, sample_movies, admin_token):
        """Test GET /movies/{movie_id} returns specific movie"""
        response = client.get(
            "/movies/1",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["movieId"] == 1
        assert data["title"] == "Toy Story (1995)"
        assert data["genres"] == "Adventure|Animation|Children|Comedy|Fantasy"

    def test_get_movie_not_found(self, client, sample_movies, admin_token):
        """Test GET /movies/{movie_id} returns 404 for non-existent ID"""
        response = client.get(
            "/movies/9999",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Movie not found"

    def test_create_movie(self, client, db, admin_token):
        """Test POST /movies creates new movie in database"""
        new_movie = {
            "movieId": 100,
            "title": "Test Movie (2024)",
            "genres": "Action|Thriller"
        }
        
        response = client.post(
            "/movies",
            json=new_movie,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["movieId"] == 100
        assert data["title"] == "Test Movie (2024)"
        assert data["genres"] == "Action|Thriller"
        
        # Verify in database
        get_response = client.get(
            "/movies/100",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()["title"] == "Test Movie (2024)"

    def test_create_movie_duplicate(self, client, sample_movies, admin_token):
        """Test POST /movies returns 400 for duplicate movieId"""
        duplicate_movie = {
            "movieId": 1,
            "title": "Duplicate Movie",
            "genres": "Drama"
        }
        
        response = client.post(
            "/movies",
            json=duplicate_movie,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "Movie already exists"

    def test_update_movie(self, client, sample_movies, admin_token):
        """Test PUT /movies/{movie_id} updates movie in database"""
        updated_data = {
            "title": "Updated Toy Story (1995)",
            "genres": "Animation|Comedy"
        }
        
        response = client.put(
            "/movies/1",
            json=updated_data,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["movieId"] == 1
        assert data["title"] == "Updated Toy Story (1995)"
        assert data["genres"] == "Animation|Comedy"
        
        # Verify change persisted
        get_response = client.get(
            "/movies/1",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert get_response.json()["title"] == "Updated Toy Story (1995)"

    def test_update_movie_not_found(self, client, sample_movies, admin_token):
        """Test PUT /movies/{movie_id} returns 404 for non-existent ID"""
        updated_data = {
            "title": "Non-existent Movie",
            "genres": "Drama"
        }
        
        response = client.put(
            "/movies/9999",
            json=updated_data,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Movie not found"

    def test_delete_movie(self, client, sample_movies, admin_token):
        """Test DELETE /movies/{movie_id} removes movie from database"""
        response = client.delete(
            "/movies/1",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify movie was deleted
        get_response = client.get(
            "/movies/1",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
        
        # Verify other movies still exist
        list_response = client.get(
            "/movies",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert len(list_response.json()) == 2

    def test_delete_movie_not_found(self, client, sample_movies, admin_token):
        """Test DELETE /movies/{movie_id} returns 404 for non-existent ID"""
        response = client.delete(
            "/movies/9999",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Movie not found"
