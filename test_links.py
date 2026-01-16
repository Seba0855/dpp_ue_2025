import pytest
from fastapi import status


class TestLinksEndpoints:
    """Integration tests for Links CRUD endpoints"""

    def test_get_links_list(self, client, sample_links, admin_token):
        """Test GET /links returns all links from fixtures"""
        response = client.get(
            "/links",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        assert data[0]["movieId"] == 1
        assert data[0]["imdbId"] == "0114709"
        assert data[0]["tmdbId"] == "862"

    def test_get_link_by_id(self, client, sample_links, admin_token):
        """Test GET /links/{movie_id} returns specific link"""
        response = client.get(
            "/links/1",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["movieId"] == 1
        assert data["imdbId"] == "0114709"
        assert data["tmdbId"] == "862"

    def test_get_link_not_found(self, client, sample_links, admin_token):
        """Test GET /links/{movie_id} returns 404 for non-existent ID"""
        response = client.get(
            "/links/9999",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Link not found"

    def test_create_link(self, client, db, admin_token):
        """Test POST /links creates new link in database"""
        new_link = {
            "movieId": 100,
            "imdbId": "1234567",
            "tmdbId": "9999"
        }
        
        response = client.post(
            "/links",
            json=new_link,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["movieId"] == 100
        assert data["imdbId"] == "1234567"
        assert data["tmdbId"] == "9999"
        
        # Verify in database
        get_response = client.get(
            "/links/100",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()["imdbId"] == "1234567"

    def test_create_link_duplicate(self, client, sample_links, admin_token):
        """Test POST /links returns 400 for duplicate movieId"""
        duplicate_link = {
            "movieId": 1,
            "imdbId": "9999999",
            "tmdbId": "8888"
        }
        
        response = client.post(
            "/links",
            json=duplicate_link,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "Link already exists"

    def test_update_link(self, client, sample_links, admin_token):
        """Test PUT /links/{movie_id} updates link in database"""
        updated_data = {
            "imdbId": "9999999",
            "tmdbId": "1111"
        }
        
        response = client.put(
            "/links/1",
            json=updated_data,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["movieId"] == 1
        assert data["imdbId"] == "9999999"
        assert data["tmdbId"] == "1111"
        
        # Verify change persisted
        get_response = client.get(
            "/links/1",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert get_response.json()["imdbId"] == "9999999"

    def test_update_link_not_found(self, client, sample_links, admin_token):
        """Test PUT /links/{movie_id} returns 404 for non-existent ID"""
        updated_data = {
            "imdbId": "0000000",
            "tmdbId": "0000"
        }
        
        response = client.put(
            "/links/9999",
            json=updated_data,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Link not found"

    def test_delete_link(self, client, sample_links, admin_token):
        """Test DELETE /links/{movie_id} removes link from database"""
        response = client.delete(
            "/links/1",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify link was deleted
        get_response = client.get(
            "/links/1",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
        
        # Verify other links still exist
        list_response = client.get(
            "/links",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert len(list_response.json()) == 2

    def test_delete_link_not_found(self, client, sample_links, admin_token):
        """Test DELETE /links/{movie_id} returns 404 for non-existent ID"""
        response = client.delete(
            "/links/9999",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Link not found"
