# backend/app/schemas.py
from datetime import date, datetime
from typing import Optional, List, Any, Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict

Units = Literal["standard", "metric", "imperial"]

class LocationQuery(BaseModel):
    query: Optional[str] = Field(default=None, description="Free-text like city, landmark, etc.")
    zip_code: Optional[str] = Field(default=None, description="Zip or postal code")
    country_code: Optional[str] = Field(default=None, description="Country code for zip e.g. US/IN")
    lat: Optional[float] = None
    lon: Optional[float] = None
    units: Units = "metric"

    @field_validator("lat", "lon")
    @classmethod
    def _coord_bounds(cls, v, info):
        if v is None:
            return v
        if info.field_name == "lat" and not (-90 <= v <= 90):
            raise ValueError("lat must be between -90 and 90")
        if info.field_name == "lon" and not (-180 <= v <= 180):
            raise ValueError("lon must be between -180 and 180")
        return v

    @field_validator("query")
    @classmethod
    def _query_strip(cls, v):
        return v.strip() if isinstance(v, str) else v

    @field_validator("zip_code")
    @classmethod
    def _zip_strip(cls, v):
        return v.strip() if isinstance(v, str) else v

    def has_location(self) -> bool:
        return bool(self.query or self.zip_code or (self.lat is not None and self.lon is not None))


class CurrentWeatherResponse(BaseModel):
    source: str
    location: dict
    weather: dict


class ForecastRequest(LocationQuery):
    days: int = Field(default=5, ge=1, le=5, description="Number of days (1-5)")


class ForecastResponse(BaseModel):
    source: str
    location: dict
    forecast: List[dict]


class GeocodeRequest(BaseModel):
    query: str = Field(..., min_length=2, description="Free-text location")


class GeocodeCandidate(BaseModel):
    formatted: str
    lat: float
    lon: float
    confidence: Optional[float] = None
    components: Optional[dict] = None


class GeocodeResponse(BaseModel):
    candidates: List[GeocodeCandidate]

# CRUD Weather History

class WeatherHistoryBase(BaseModel):
    location_name: str = Field(..., min_length=2, max_length=100)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    weather_data: Optional[Any] = None

    @field_validator("latitude", "longitude")
    @classmethod
    def _coord_bounds(cls, v, info):
        if v is None:
            return v
        if info.field_name == "latitude" and not (-90 <= v <= 90):
            raise ValueError("latitude must be between -90 and 90")
        if info.field_name == "longitude" and not (-180 <= v <= 180):
            raise ValueError("longitude must be between -180 and 180")
        return v


class WeatherHistoryCreate(WeatherHistoryBase):
    temperature: float = Field(..., description="Temperature in selected units")
    humidity: float = Field(..., description="Humidity percentage")
    recorded_at: datetime = Field(..., description="When this weather reading was recorded")

    @field_validator("temperature", "humidity")
    @classmethod
    def _must_be_real_number(cls, v):
        if not isinstance(v, (float, int)):
            raise ValueError("Must be a number")
        return float(v)


class WeatherHistoryRead(WeatherHistoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    recorded_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class WeatherHistoryUpdate(BaseModel):
    location_name: Optional[str] = Field(None, min_length=2, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    weather_data: Optional[Any] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    recorded_at: Optional[datetime] = None
