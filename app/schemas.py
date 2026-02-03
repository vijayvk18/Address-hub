"""
Pydantic schemas for request/response validation.
"""

from typing import Optional

from pydantic import BaseModel, Field, validator


class AddressBase(BaseModel):
    """Base schema with common address fields."""

    street: str = Field(..., min_length=1, max_length=200, description="Street address")
    city: str = Field(..., min_length=1, max_length=100, description="City name")
    state: str = Field(..., min_length=1, max_length=100, description="State/Province name")
    zip_code: str = Field(..., min_length=1, max_length=20, description="Postal/ZIP code")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate (-180 to 180)")

    @validator("latitude", "longitude")
    def validate_coordinates(cls, v):
        """Validate that coordinates are within valid ranges."""
        if isinstance(v, (int, float)):
            return float(v)
        raise ValueError("Coordinates must be numeric values")


class AddressCreate(AddressBase):
    """Schema for creating a new address."""

    pass


class AddressUpdate(BaseModel):
    """Schema for updating an existing address (all fields optional)."""

    street: Optional[str] = Field(None, min_length=1, max_length=200)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=1, max_length=100)
    zip_code: Optional[str] = Field(None, min_length=1, max_length=20)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

    @validator("latitude", "longitude")
    def validate_coordinates(cls, v):
        """Validate that coordinates are within valid ranges."""
        if v is None:
            return v
        if isinstance(v, (int, float)):
            return float(v)
        raise ValueError("Coordinates must be numeric values")


class AddressResponse(AddressBase):
    """Schema for address response (includes ID)."""

    id: int

    class Config:
        from_attributes = True


class DistanceSearchRequest(BaseModel):
    """Schema for distance-based search request."""

    latitude: float = Field(..., ge=-90, le=90, description="Reference latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Reference longitude")
    distance_km: float = Field(..., gt=0, description="Maximum distance in kilometers")

    @validator("latitude", "longitude")
    def validate_coordinates(cls, v):
        """Validate that coordinates are within valid ranges."""
        if isinstance(v, (int, float)):
            return float(v)
        raise ValueError("Coordinates must be numeric values")
