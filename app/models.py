"""
SQLAlchemy database models.
"""

from sqlalchemy import Column, Float, Integer, String

from app.database import Base


class Address(Base):
    """
    Address model representing an address entry in the database.

    Attributes:
        id: Primary key, auto-incrementing integer
        street: Street address
        city: City name
        state: State/Province name
        zip_code: Postal/ZIP code
        latitude: Latitude coordinate (decimal degrees)
        longitude: Longitude coordinate (decimal degrees)
    """

    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, nullable=False, index=True)
    city = Column(String, nullable=False, index=True)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

