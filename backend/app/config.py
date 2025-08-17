# backend/app/config.py
# Config vars (API keys, DB URL)
from pydantic_settings import BaseSettings
from pydantic import AnyUrl, Field

class Settings(BaseSettings):
    # Phase 1/2/3 keys
    OPENWEATHER_API_KEY: str = Field(default="", description="OpenWeather API key")
    OPENCAGE_API_KEY: str = Field(default="", description="OpenCage API key")
    YOUTUBE_API_KEY: str = Field(default="", description="YouTube Data API v3 key")

    # DB + CORS
    DATABASE_URL: AnyUrl | str = Field(default="sqlite:///./weather.db")
    ALLOWED_ORIGINS: str = Field(default="http://localhost:5173")

    # Tile server template (MUST include {z}/{x}/{y}.png)
    # Used by the server-side static map renderer (staticmap).
    TILE_SERVER_URL: str = Field(
        default="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        description="URL template for raster tiles used by static map renderer",
    )

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
