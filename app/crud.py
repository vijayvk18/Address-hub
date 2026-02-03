"""
CRUD operations for address management.
"""

import logging
import math
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Address
from app.schemas import AddressCreate, AddressUpdate

logger = logging.getLogger(__name__)


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth using Haversine formula.

    Args:
        lat1: Latitude of first point
        lon1: Longitude of first point
        lat2: Latitude of second point
        lon2: Longitude of second point

    Returns:
        Distance in kilometers
    """
    # Earth's radius in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


def create_address(db: Session, address: AddressCreate) -> Address:
    """
    Create a new address in the database.

    Args:
        db: Database session
        address: Address data to create

    Returns:
        Created Address object
    """
    logger.info(f"Creating new address: {address.street}, {address.city}")
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    logger.info(f"Address created successfully with ID: {db_address.id}")
    return db_address


def get_address(db: Session, address_id: int) -> Optional[Address]:
    """
    Retrieve an address by ID.

    Args:
        db: Database session
        address_id: ID of the address to retrieve

    Returns:
        Address object if found, None otherwise
    """
    logger.debug(f"Retrieving address with ID: {address_id}")
    address = db.query(Address).filter(Address.id == address_id).first()
    if address:
        logger.debug(f"Address found: {address.street}, {address.city}")
    else:
        logger.debug(f"Address with ID {address_id} not found")
    return address


def get_all_addresses(db: Session, skip: int = 0, limit: int = 100) -> List[Address]:
    """
    Retrieve all addresses with pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of Address objects
    """
    logger.debug(f"Retrieving addresses (skip={skip}, limit={limit})")
    addresses = db.query(Address).offset(skip).limit(limit).all()
    logger.debug(f"Found {len(addresses)} addresses")
    return addresses


def update_address(db: Session, address_id: int, address_update: AddressUpdate) -> Optional[Address]:
    """
    Update an existing address.

    Args:
        db: Database session
        address_id: ID of the address to update
        address_update: Address data to update (only provided fields will be updated)

    Returns:
        Updated Address object if found, None otherwise
    """
    logger.info(f"Updating address with ID: {address_id}")
    db_address = get_address(db, address_id)

    if not db_address:
        logger.warning(f"Address with ID {address_id} not found for update")
        return None

    # Update only provided fields
    update_data = address_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_address, field, value)

    db.commit()
    db.refresh(db_address)
    logger.info(f"Address with ID {address_id} updated successfully")
    return db_address


def delete_address(db: Session, address_id: int) -> bool:
    """
    Delete an address from the database.

    Args:
        db: Database session
        address_id: ID of the address to delete

    Returns:
        True if address was deleted, False if not found
    """
    logger.info(f"Deleting address with ID: {address_id}")
    db_address = get_address(db, address_id)

    if not db_address:
        logger.warning(f"Address with ID {address_id} not found for deletion")
        return False

    db.delete(db_address)
    db.commit()
    logger.info(f"Address with ID {address_id} deleted successfully")
    return True


def search_addresses_by_distance(db: Session, latitude: float, longitude: float, distance_km: float) -> List[Address]:
    """
    Find all addresses within a specified distance from given coordinates.

    Args:
        db: Database session
        latitude: Reference latitude
        longitude: Reference longitude
        distance_km: Maximum distance in kilometers

    Returns:
        List of Address objects within the specified distance
    """
    logger.info(f"Searching addresses within {distance_km}km of ({latitude}, {longitude})")

    # Get all addresses from database
    all_addresses = db.query(Address).all()

    # Filter addresses by distance
    nearby_addresses = []
    for address in all_addresses:
        distance = haversine_distance(latitude, longitude, address.latitude, address.longitude)
        if distance <= distance_km:
            nearby_addresses.append(address)
            logger.debug(f"Address ID {address.id} is {distance:.2f}km away " f"(within {distance_km}km)")

    logger.info(f"Found {len(nearby_addresses)} addresses within {distance_km}km")
    return nearby_addresses
