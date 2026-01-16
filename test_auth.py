import pytest
from fastapi import status


class TestAuthEndpoints:
    """Integration tests for authentication endpoints"""

    def test_login_success(self, client, admin_user):
        """Test successful login with correct credentials"""
        response = client.post("/login", json={
            "username": "admin",
            "password": "admin123"
        })
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0

    def test_login_invalid_username(self, client, admin_user):
        """Test login with non-existent username"""
        response = client.post("/login", json={
            "username": "nonexistent",
            "password": "admin123"
        })
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Invalid credentials"

    def test_login_invalid_password(self, client, admin_user):
        """Test login with incorrect password"""
        response = client.post("/login", json={
            "username": "admin",
            "password": "wrongpassword"
        })
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Invalid credentials"

    def test_create_user_as_admin(self, client, admin_user, admin_token):
        """Test creating user with admin privileges"""
        response = client.post(
            "/users",
            json={
                "username": "newuser",
                "password": "newpass123",
                "roles": ["ROLE_USER"]
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == "newuser"
        assert data["roles"] == ["ROLE_USER"]
        assert "id" in data
        
        # Verify user can login
        login_response = client.post("/login", json={
            "username": "newuser",
            "password": "newpass123"
        })
        assert login_response.status_code == status.HTTP_200_OK

    def test_create_user_without_admin_role(self, client, regular_user, user_token):
        """Test creating user without admin privileges - should fail"""
        response = client.post(
            "/users",
            json={
                "username": "newuser",
                "password": "newpass123",
                "roles": ["ROLE_USER"]
            },
            headers={"Authorization": f"Bearer {user_token}"}
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "ROLE_ADMIN" in response.json()["detail"]

    def test_create_user_without_token(self, client, admin_user):
        """Test creating user without authentication token"""
        response = client.post(
            "/users",
            json={
                "username": "newuser",
                "password": "newpass123",
                "roles": ["ROLE_USER"]
            }
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_user_duplicate_username(self, client, admin_user, admin_token):
        """Test creating user with existing username"""
        response = client.post(
            "/users",
            json={
                "username": "admin",
                "password": "newpass123",
                "roles": ["ROLE_USER"]
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "Username already exists"

    def test_get_user_details_with_token(self, client, admin_user, admin_token):
        """Test getting user details with valid token"""
        response = client.get(
            "/user_details",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "admin"
        assert "ROLE_ADMIN" in data["roles"]
        assert "ROLE_USER" in data["roles"]

    def test_get_user_details_without_token(self, client, admin_user):
        """Test getting user details without token"""
        response = client.get("/user_details")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_user_details_with_invalid_token(self, client, admin_user):
        """Test getting user details with invalid token"""
        response = client.get(
            "/user_details",
            headers={"Authorization": "Bearer invalid_token_here"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid token" in response.json()["detail"]

    def test_regular_user_details(self, client, regular_user, user_token):
        """Test getting regular user details"""
        response = client.get(
            "/user_details",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "user"
        assert data["roles"] == ["ROLE_USER"]
        assert "ROLE_ADMIN" not in data["roles"]
