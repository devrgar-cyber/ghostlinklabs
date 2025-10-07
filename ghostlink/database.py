import datetime
import secrets
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.pool import StaticPool
from .config import config

Base = declarative_base()

def utc_now():
    """Get current UTC time in a timezone-aware way."""
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)

class ApiKey(Base):
    """Database model for API keys."""
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    user_id = Column(String, nullable=False) 
    permissions = Column(String, default="read")  # e.g., "read,write,admin"
    created_at = Column(DateTime, default=utc_now)
    expires_at = Column(DateTime, nullable=True)
    
    def has_permission(self, permission: str) -> bool:
        """Check if the API key has a specific permission."""
        if not self.permissions:
            return False
        normalized_permissions = [perm.strip() for perm in self.permissions.split(",") if perm.strip()]
        return permission in normalized_permissions
    
    def is_expired(self) -> bool:
        """Check if the API key has expired."""
        if self.expires_at is None:
            return False
        return utc_now() > self.expires_at


class Database:
    """Database manager for GhostLink."""
    
    def __init__(self, database_url: str | None = None):
        if database_url is None:
            database_url = config.DATABASE_URL

        engine_kwargs = {}
        if database_url.startswith("sqlite"):
            engine_kwargs["connect_args"] = {"check_same_thread": False}
            if database_url.endswith(":memory:"):
                engine_kwargs["poolclass"] = StaticPool

        self.engine = create_engine(database_url, **engine_kwargs)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self) -> Session:
        """Get a database session."""
        return self.SessionLocal()
    
    def create_api_key(
        self,
        user_id: str,
        permissions: str = "read",
        expires_at: Optional[datetime.datetime] = None,
    ) -> ApiKey:
        """Create a new API key."""
        if expires_at is None:
            default_days = getattr(config, "API_KEY_EXPIRATION_DAYS", None)
            if default_days is not None:
                expires_at = utc_now() + datetime.timedelta(days=default_days)

        key = secrets.token_urlsafe(32)
        api_key = ApiKey(
            key=key,
            user_id=user_id,
            permissions=permissions,
            expires_at=expires_at
        )
        
        with self.get_session() as session:
            session.add(api_key)
            session.commit()
            session.refresh(api_key)
            return api_key
    
    def get_api_key(self, key: str) -> Optional[ApiKey]:
        """Retrieve an API key by its value."""
        with self.get_session() as session:
            return session.query(ApiKey).filter_by(key=key).first()
    
    def validate_api_key(self, key: str, required_permission: str = "read") -> Optional[ApiKey]:
        """Validate an API key and check permissions."""
        api_key = self.get_api_key(key)
        if not api_key:
            return None

        if api_key.is_expired():
            return None

        if not api_key.has_permission(required_permission):
            return None

        return api_key
