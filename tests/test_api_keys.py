import datetime
import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ghostlink.main import app, set_db
from ghostlink.database import Database, ApiKey, utc_now
from ghostlink.config import config


@pytest.fixture(scope="session", autouse=True)
def setup_global_test_database():
    """Setup a global test database for the entire test session."""
    # Create test database and set it
    test_db = Database("sqlite:///:memory:")
    set_db(test_db)


@pytest.fixture(autouse=True)
def clear_test_data():
    """Clear test data before each test."""
    # Clear application state
    from ghostlink import main
    main.items.clear()
    main.ipfs.storage.clear()
    
    # Clear database data
    db = main.get_db()
    with db.get_session() as session:
        session.query(ApiKey).delete()
        session.commit()


client = TestClient(app)


class TestApiKeyManagement:
    """Test API key creation and management."""
    
    def test_create_api_key(self):
        """Test creating a new API key."""
        payload = {
            "user_id": "test_user",
            "permissions": "read,write",
        }
        response = client.post("/api_keys", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert data["user_id"] == "test_user"
        assert data["permissions"] == "read,write"
        assert "key" in data
        assert len(data["key"]) > 20  # Token should be substantial length
        assert "id" in data
        assert "created_at" in data
        assert data["expires_at"] is not None

    def test_default_expiration_applied_and_honored(self):
        """Test that default expiration is set and validated when not provided."""
        payload = {
            "user_id": "default_expiry_user",
            "permissions": "read, write",
        }
        response = client.post("/api_keys", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert data["expires_at"] is not None

        expires_at = datetime.datetime.fromisoformat(data["expires_at"])
        expected_expiry = utc_now() + datetime.timedelta(days=config.API_KEY_EXPIRATION_DAYS)
        # Allow a small delta for processing time differences
        assert abs((expires_at - expected_expiry).total_seconds()) < 10

        validation_response = client.get("/api_keys/validate", headers={"X-API-Key": data["key"]})
        assert validation_response.status_code == 200

    def test_database_layer_applies_default_expiration(self):
        """Ensure the database helper applies the default expiration policy."""
        db = Database("sqlite:///:memory:")
        try:
            created_key = db.create_api_key(user_id="db_default_user", permissions="read")

            assert created_key.expires_at is not None
            expected_expiry = utc_now() + datetime.timedelta(days=config.API_KEY_EXPIRATION_DAYS)
            assert abs((created_key.expires_at - expected_expiry).total_seconds()) < 10
        finally:
            db.engine.dispose()

    def test_create_api_key_with_expiration(self):
        """Test creating an API key with expiration date."""
        future_date = (utc_now() + datetime.timedelta(days=30)).isoformat()
        payload = {
            "user_id": "test_user",
            "permissions": "admin",
            "expires_at": future_date
        }
        response = client.post("/api_keys", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["permissions"] == "admin"
        assert data["expires_at"] is not None
    
    def test_validate_api_key_endpoint(self):
        """Test the API key validation endpoint."""
        # First create an API key
        create_response = client.post("/api_keys", json={
            "user_id": "test_user",
            "permissions": "read"
        })
        api_key = create_response.json()["key"]
        
        # Test validation with valid key
        response = client.get("/api_keys/validate", headers={"X-API-Key": api_key})
        assert response.status_code == 200
        
        data = response.json()
        assert data["valid"] is True
        assert data["user_id"] == "test_user"
        assert data["permissions"] == "read"
    
    def test_validate_invalid_api_key(self):
        """Test validation with invalid API key."""
        response = client.get("/api_keys/validate", headers={"X-API-Key": "invalid-key"})
        assert response.status_code == 403
        assert "Invalid or expired API key" in response.json()["detail"]
    
    def test_validate_missing_api_key(self):
        """Test validation without API key header."""
        response = client.get("/api_keys/validate")
        assert response.status_code == 400
        assert "API key required" in response.json()["detail"]


class TestApiKeyAuthentication:
    """Test API key authentication on existing endpoints."""
    
    def setup_method(self):
        """Setup test data for each test."""
        # Create test API keys
        self.read_key_response = client.post("/api_keys", json={
            "user_id": "read_user",
            "permissions": "read"
        })
        self.read_key = self.read_key_response.json()["key"]
        
        self.write_key_response = client.post("/api_keys", json={
            "user_id": "write_user", 
            "permissions": "read,write"
        })
        self.write_key = self.write_key_response.json()["key"]
        
        self.admin_key_response = client.post("/api_keys", json={
            "user_id": "admin_user",
            "permissions": "read,write,admin"
        })
        self.admin_key = self.admin_key_response.json()["key"]
    
    def test_create_item_without_api_key(self):
        """Test creating item without API key (should work)."""
        payload = {"name": "test_item", "value": 42}
        response = client.post("/items", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "test_item"
        assert "created_by" not in data
    
    def test_create_item_with_valid_api_key(self):
        """Test creating item with valid API key."""
        payload = {"name": "test_item", "value": 42}
        response = client.post("/items", json=payload, headers={"X-API-Key": self.write_key})
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "test_item"
        assert data["created_by"] == "write_user"
    
    def test_create_item_with_invalid_api_key(self):
        """Test creating item with invalid API key."""
        payload = {"name": "test_item", "value": 42}
        response = client.post("/items", json=payload, headers={"X-API-Key": "invalid-key"})
        assert response.status_code == 403
        assert "Invalid or expired API key" in response.json()["detail"]
    
    def test_get_items_with_api_key(self):
        """Test getting items with API key."""
        # Create an item first
        client.post("/items", json={"name": "test", "value": 1})
        
        response = client.get("/items", headers={"X-API-Key": self.read_key})
        assert response.status_code == 200
        assert len(response.json()) == 1
    
    def test_external_api_requires_api_key(self):
        """Test that external API endpoint requires API key."""
        # Without API key
        response = client.get("/external_api/data")
        assert response.status_code == 401
        assert "API key required" in response.json()["detail"]
        
        # With valid API key
        response = client.get("/external_api/data", headers={"X-API-Key": self.read_key})
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Secured data access"
        assert data["user_id"] == "read_user"
        assert "items_count" in data
    
    def test_external_api_admin_permissions(self):
        """Test admin permissions on external API."""
        # Create some test data
        client.post("/items", json={"name": "regular", "value": 1})
        client.post("/items", json={"name": "sensitive", "value": 2, "sensitive": True})
        
        # Test with read permissions (should not see sensitive data)
        response = client.get("/external_api/data", headers={"X-API-Key": self.read_key})
        assert response.status_code == 200
        data = response.json()
        assert len([item for item in data["data"] if item.get("sensitive")]) == 0
        
        # Test with admin permissions (should see all data)
        response = client.get("/external_api/data", headers={"X-API-Key": self.admin_key})
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 2


class TestApiKeyPermissions:
    """Test permission checking functionality."""
    
    def test_api_key_has_permission(self):
        """Test the has_permission method."""
        api_key = ApiKey(permissions="read,write")

        assert api_key.has_permission("read") is True
        assert api_key.has_permission("write") is True
        assert api_key.has_permission("admin") is False

        # Test permissions with spaces around commas
        spaced_permissions_key = ApiKey(permissions="read, write, admin")
        assert spaced_permissions_key.has_permission("read") is True
        assert spaced_permissions_key.has_permission("write") is True
        assert spaced_permissions_key.has_permission("admin") is True

        # Test empty permissions
        empty_key = ApiKey(permissions="")
        assert empty_key.has_permission("read") is False

        # Test None permissions
        none_key = ApiKey(permissions=None)
        assert none_key.has_permission("read") is False
    
    def test_api_key_expiration(self):
        """Test API key expiration functionality."""
        from ghostlink.database import utc_now
        
        # Non-expired key
        future_date = utc_now() + datetime.timedelta(days=1)
        valid_key = ApiKey(expires_at=future_date)
        assert valid_key.is_expired() is False
        
        # Expired key
        past_date = utc_now() - datetime.timedelta(days=1)
        expired_key = ApiKey(expires_at=past_date)
        assert expired_key.is_expired() is True
        
        # Key with no expiration
        no_expiry_key = ApiKey(expires_at=None)
        assert no_expiry_key.is_expired() is False


class TestBackwardCompatibility:
    """Test that existing functionality still works without API keys."""
    
    def test_all_endpoints_work_without_api_keys(self):
        """Test that all original endpoints still work without API keys."""
        # Test create item
        response = client.post("/items", json={"name": "test", "value": 42})
        assert response.status_code == 200
        
        # Test get items
        response = client.get("/items")
        assert response.status_code == 200
        
        # Test reasoning
        response = client.post("/reasoning/", json={"text": "test"})
        assert response.status_code == 200
        
        # Test IPFS store
        response = client.post("/ipfs/store", json={"data": "test"})
        assert response.status_code == 200
        cid = response.json()["cid"]
        
        # Test IPFS retrieve
        response = client.get(f"/ipfs/{cid}")
        assert response.status_code == 200
        assert response.json()["data"] == "test"