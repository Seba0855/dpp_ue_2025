import pytest
from fastapi import status


class TestTagsEndpoints:
    """Integration tests for Tags CRUD endpoints"""

    def test_get_tags_list(self, client, sample_tags):
        """Test GET /tags returns all tags from fixtures"""
        response = client.get("/tags")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        assert data[0]["userId"] == 2
        assert data[0]["movieId"] == 60756
        assert data[0]["tag"] == "funny"

    def test_get_tag_by_id(self, client, sample_tags):
        """Test GET /tags/{tag_id} returns specific tag"""
        tag_id = sample_tags[0].id
        response = client.get(f"/tags/{tag_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == tag_id
        assert data["userId"] == 2
        assert data["movieId"] == 60756
        assert data["tag"] == "funny"
        assert data["timestamp"] == 1445714994

    def test_get_tag_not_found(self, client, sample_tags):
        """Test GET /tags/{tag_id} returns 404 for non-existent ID"""
        response = client.get("/tags/9999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Tag not found"

    def test_create_tag(self, client, db):
        """Test POST /tags creates new tag in database"""
        new_tag = {
            "userId": 10,
            "movieId": 100,
            "tag": "awesome",
            "timestamp": 1234567890
        }
        
        response = client.post("/tags", json=new_tag)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["userId"] == 10
        assert data["movieId"] == 100
        assert data["tag"] == "awesome"
        assert data["timestamp"] == 1234567890
        assert "id" in data
        
        # Verify in database
        get_response = client.get(f"/tags/{data['id']}")
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()["tag"] == "awesome"

    def test_update_tag(self, client, sample_tags):
        """Test PUT /tags/{tag_id} updates tag in database"""
        tag_id = sample_tags[0].id
        updated_data = {
            "userId": 2,
            "movieId": 60756,
            "tag": "hilarious",
            "timestamp": 999999999
        }
        
        response = client.put(f"/tags/{tag_id}", json=updated_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == tag_id
        assert data["tag"] == "hilarious"
        assert data["timestamp"] == 999999999
        
        # Verify change persisted
        get_response = client.get(f"/tags/{tag_id}")
        assert get_response.json()["tag"] == "hilarious"

    def test_update_tag_partial(self, client, sample_tags):
        """Test PUT /tags/{tag_id} with partial update"""
        tag_id = sample_tags[0].id
        updated_data = {
            "tag": "very funny"
        }
        
        response = client.put(f"/tags/{tag_id}", json=updated_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["tag"] == "very funny"
        assert data["userId"] == 2  # Original value preserved
        assert data["movieId"] == 60756  # Original value preserved

    def test_update_tag_not_found(self, client, sample_tags):
        """Test PUT /tags/{tag_id} returns 404 for non-existent ID"""
        updated_data = {
            "tag": "non-existent"
        }
        
        response = client.put("/tags/9999", json=updated_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Tag not found"

    def test_delete_tag(self, client, sample_tags):
        """Test DELETE /tags/{tag_id} removes tag from database"""
        tag_id = sample_tags[0].id
        response = client.delete(f"/tags/{tag_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify tag was deleted
        get_response = client.get(f"/tags/{tag_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
        
        # Verify other tags still exist
        list_response = client.get("/tags")
        assert len(list_response.json()) == 2

    def test_delete_tag_not_found(self, client, sample_tags):
        """Test DELETE /tags/{tag_id} returns 404 for non-existent ID"""
        response = client.delete("/tags/9999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Tag not found"
