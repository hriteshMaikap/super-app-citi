"""
Core configuration for the Super App Backend
Banking-grade security settings and environment management
"""
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator
import secrets
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    # Application
    app_name: str = os.getenv("APP_NAME", "Super App Backend")
    app_version: str = os.getenv("APP_VERSION", "0.1.0")
    debug: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    environment: str = os.getenv("ENVIRONMENT", "production")
    
    # Security - Banking Grade
    secret_key: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    # Database - MySQL Configuration
    mysql_user: str = os.getenv("MYSQL_USER", "root")
    mysql_pass: str = os.getenv("MYSQL_PASS", "")
    mysql_host: str = os.getenv("MYSQL_HOST", "127.0.0.1")
    mysql_port: int = int(os.getenv("MYSQL_PORT", "3306"))
    mysql_db: str = os.getenv("MYSQL_DB", "superapp_db")
    
    @property
    def database_url(self) -> str:
        return f"mysql+aiomysql://{self.mysql_user}:{self.mysql_pass}@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}"
    
    # MongoDB Configuration (E-commerce)
    mongodb_uri: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    mongodb_db_name: str = os.getenv("MONGODB_DB_NAME", "superapp_ecommerce")
    mongodb_schema_sample_size: int = int(os.getenv("MONGODB_SCHEMA_SAMPLE_SIZE", "100"))
    
    # Encryption
    encryption_key: str = os.getenv("ENCRYPTION_KEY", secrets.token_urlsafe(32))
    salt_rounds: int = int(os.getenv("SALT_ROUNDS", "12"))
    
    # Rate Limiting
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    rate_limit_window: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000"]
    
    @field_validator("secret_key")
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError("Secret key must be at least 32 characters for banking security")
        return v
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False
    }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()