"""
Address-related API routes.
"""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import AddressCreate, AddressResponse, AddressUpdate, DistanceSearchRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post(
    "",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new address",
    description="Create a new address entry with street, city, state, zip code, and coordinates",
)
async def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    """
    Create a new address.

    - **street**: Street address (required)
    - **city**: City name (required)
    - **state**: State/Province name (required)
    - **zip_code**: Postal/ZIP code (required)
    - **latitude**: Latitude coordinate between -90 and 90 (required)
    - **longitude**: Longitude coordinate between -180 and 180 (required)
    """
    try:
        logger.info(f"POST /addresses - Creating address: {address.street}, {address.city}")
        db_address = crud.create_address(db=db, address=address)
        return db_address
    except Exception as e:
        logger.error(f"Error creating address: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create address")


@router.get(
    "",
    response_model=List[AddressResponse],
    summary="Get all addresses",
    description="Retrieve all addresses with optional pagination",
)
async def get_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all addresses.

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100, max: 1000)
    """
    if limit > 1000:
        limit = 1000
    logger.info(f"GET /addresses - Retrieving addresses (skip={skip}, limit={limit})")
    addresses = crud.get_all_addresses(db=db, skip=skip, limit=limit)
    return addresses


@router.get(
    "/{address_id}",
    response_model=AddressResponse,
    summary="Get address by ID",
    description="Retrieve a specific address by its ID",
)
async def get_address(address_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an address by ID.

    - **address_id**: The ID of the address to retrieve
    """
    logger.info(f"GET /addresses/{address_id} - Retrieving address")
    db_address = crud.get_address(db=db, address_id=address_id)
    if db_address is None:
        logger.warning(f"Address with ID {address_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Address with ID {address_id} not found")
    return db_address


@router.put(
    "/{address_id}",
    response_model=AddressResponse,
    summary="Update an address",
    description="Update an existing address. Only provided fields will be updated.",
)
async def update_address(address_id: int, address_update: AddressUpdate, db: Session = Depends(get_db)):
    """
    Update an existing address.

    - **address_id**: The ID of the address to update
    - All fields are optional - only provided fields will be updated
    """
    logger.info(f"PUT /addresses/{address_id} - Updating address")
    db_address = crud.update_address(db=db, address_id=address_id, address_update=address_update)
    if db_address is None:
        logger.warning(f"Address with ID {address_id} not found for update")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Address with ID {address_id} not found")
    return db_address


@router.delete(
    "/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an address",
    description="Delete an address by its ID",
)
async def delete_address(address_id: int, db: Session = Depends(get_db)):
    """
    Delete an address.

    - **address_id**: The ID of the address to delete
    """
    logger.info(f"DELETE /addresses/{address_id} - Deleting address")
    deleted = crud.delete_address(db=db, address_id=address_id)
    if not deleted:
        logger.warning(f"Address with ID {address_id} not found for deletion")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Address with ID {address_id} not found")
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)


@router.post(
    "/search",
    response_model=List[AddressResponse],
    summary="Search addresses by distance",
    description="Find all addresses within a specified distance from given coordinates",
)
async def search_addresses_by_distance(search_request: DistanceSearchRequest, db: Session = Depends(get_db)):
    """
    Search for addresses within a specified distance from given coordinates.

    - **latitude**: Reference latitude (-90 to 90)
    - **longitude**: Reference longitude (-180 to 180)
    - **distance_km**: Maximum distance in kilometers (must be > 0)

    Returns all addresses within the specified distance using the Haversine formula.
    """
    logger.info(
        f"POST /addresses/search - Searching within {search_request.distance_km}km "
        f"of ({search_request.latitude}, {search_request.longitude})"
    )
    addresses = crud.search_addresses_by_distance(
        db=db,
        latitude=search_request.latitude,
        longitude=search_request.longitude,
        distance_km=search_request.distance_km,
    )
    return addresses
