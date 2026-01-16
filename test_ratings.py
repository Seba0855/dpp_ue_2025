import pytest
from fastapi import status


class TestRatingsEndpoints:
    """Integration tests for Ratings CRUD endpoints"""

    def test_get_ratings_list(self, client, sample_ratings, admin_token):
        """Test GET /ratings returns all ratings from fixtures"""
        response = client.get(
            "/ratings",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        assert data[0]["userId"] == 1
        assert data[0]["movieId"] == 1
        assert data[0]["rating"] == 4.0

    def test_get_rating_by_id(self, client, sample_ratings, admin_token):
        """Test GET /ratings/{rating_id} returns specific rating"""
        rating_id = sample_ratings[0].id
        response = client.get(
            f"/ratings/{rating_id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == rating_id
        assert data["userId"] == 1
        assert data["movieId"] == 1
        assert data["rating"] == 4.0
        assert data["timestamp"] == 964982703

    def test_get_rating_not_found(self, client, sample_ratings, admin_token):
        """Test GET /ratings/{rating_id} returns 404 for non-existent ID"""
        response = client.get(
            "/ratings/9999",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Rating not found"

    def test_create_rating(self, client, db, admin_token):
        """Test POST /ratings creates new rating in database"""
        new_rating = {
            "userId": 5,
            "movieId": 10,
            "rating": 3.5,
            "timestamp": 1234567890
        }
        
        response = client.post(
            "/ratings",
            json=new_rating,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["userId"] == 5
        assert data["movieId"] == 10
        assert data["rating"] == 3.5
        assert data["timestamp"] == 1234567890
        assert "id" in data
        
        # Verify in database
        get_response = client.get(
            f"/ratings/{data['id']}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()["rating"] == 3.5

    def test_update_rating(self, client, sample_ratings, admin_token):
        """Test PUT /ratings/{rating_id} updates rating in database"""
        rating_id = sample_ratings[0].id
        updated_data = {
            "userId": 1,
            "movieId": 1,
            "rating": 5.0,
            "timestamp": 999999999
        }
        
        response = client.put(
            f"/ratings/{rating_id}",
            json=updated_data,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == rating_id
        assert data["rating"] == 5.0
        assert data["timestamp"] == 999999999
        
        # Verify change persisted
        get_response = client.get(
            f"/ratings/{rating_id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert get_response.json()["rating"] == 5.0

    def test_update_rating_partial(self, client, sample_ratings, admin_token):
        """Test PUT /ratings/{rating_id} with partial update"""
        rating_id = sample_ratings[0].id
        updated_data = {
            "rating": 2.5
        }
        
        response = client.put(
            f"/ratings/{rating_id}",
            json=updated_data,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["rating"] == 2.5
        assert data["userId"] == 1  # Original value preserved
        assert data["movieId"] == 1  # Original value preserved

    def test_update_rating_not_found(self, client, sample_ratings, admin_token):
        """Test PUT /ratings/{rating_id} returns 404 for non-existent ID"""
        updated_data = {
            "rating": 3.0
        }
        
        response = client.put(
            "/ratings/9999",
            json=updated_data,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Rating not found"

    def test_delete_rating(self, client, sample_ratings, admin_token):
        """Test DELETE /ratings/{rating_id} removes rating from database"""
        rating_id = sample_ratings[0].id
        response = client.delete(
            f"/ratings/{rating_id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify rating was deleted
        get_response = client.get(
            f"/ratings/{rating_id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
        
        # Verify other ratings still exist
        list_response = client.get(
            "/ratings",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert len(list_response.json()) == 2

    def test_delete_rating_not_found(self, client, sample_ratings, admin_token):
        """Test DELETE /ratings/{rating_id} returns 404 for non-existent ID"""
        response = client.delete(
            "/ratings/9999",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Rating not found"
