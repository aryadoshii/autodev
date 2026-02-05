from pydantic import BaseSettings, Field
from typing import List, Optional
import os

class Settings(BaseSettings):
    """
    Application settings class using Pydantic BaseSettings.
    
    This class defines all application configuration parameters with
    appropriate validation and default values based on the environment.
    """
    
    # Database Configuration
    database_url: str = Field(
        ..., 
        description="Database connection URL"
    )
    
    # JWT Configuration
    jwt_secret_key: str = Field(
        ...,
        description="Secret key for JWT token signing"
    )
    jwt_algorithm: str = Field(
        "HS256",
        description="JWT token algorithm"
    )
    jwt_access_token_expire_minutes: int = Field(
        30,
        description="Access token expiration time in minutes"
    )
    
    # CORS Configuration
    cors_origins: List[str] = Field(
        [],
        description="List of allowed CORS origins"
    )
    
    # Environment Configuration
    environment: str = Field(
        "development",
        description="Application environment (development/production)"
    )
    
    # Environment variable loading
    class Config:
        """Pydantic configuration for Settings class."""
        env_file = ".env" if os.getenv("ENVIRONMENT") != "production" else ".env.production"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

# Create a global instance of the settings
settings = Settings()

# Example usage:
"""
# In your application code:
from config import settings

# Access configuration values
db_url = settings.database_url
jwt_secret = settings.jwt_secret_key
cors_origins = settings.cors_origins

# Check environment
if settings.is_development:
    print("Running in development mode")
elif settings.is_production:
    print("Running in production mode")
"""