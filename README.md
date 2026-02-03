# Address Book API

A RESTful API application built with FastAPI for managing addresses with coordinate-based search functionality.

## Features

- **Create, Read, Update, Delete (CRUD)** operations for addresses
- **Coordinate-based storage** - Each address includes latitude and longitude
- **Distance-based search** - Find addresses within a specified distance from given coordinates using the Haversine formula
- **Input validation** - Comprehensive validation using Pydantic schemas
- **SQLite database** - Lightweight, file-based database storage
- **Interactive API documentation** - Built-in Swagger UI and ReDoc
- **Logging** - Comprehensive logging for debugging and monitoring

## Project Structure

```
fast-api-project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration and session management
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── crud.py              # CRUD operations and business logic
│   └── routers/
│       ├── __init__.py
│       └── addresses.py     # Address-related API routes
├── venv/                    # Virtual environment (created during setup)
├── requirements.txt         # Python dependencies
├── setup_venv.ps1          # Windows PowerShell script for venv setup
├── setup_venv.sh           # Linux/macOS script for venv setup
├── README.md               # This file
└── .gitignore              # Git ignore file
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation & Setup

1. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**
   
   On Windows (PowerShell):
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   On Windows (Command Prompt):
   ```cmd
   venv\Scripts\activate.bat
   ```
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

3. **Upgrade pip (recommended)**
   ```bash
   python -m pip install --upgrade pip
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Start the server

**Important:** Make sure your virtual environment is activated before running the application.

```bash
uvicorn app.main:app --reload
```

The `--reload` flag enables auto-reload on code changes (useful for development).

### Access the API

Once the server is running, you can access:

- **API Base URL**: http://127.0.0.1:8000
- **Interactive API Documentation (Swagger UI)**: http://127.0.0.1:8000/docs
- **Alternative API Documentation (ReDoc)**: http://127.0.0.1:8000/redoc
- **Health Check**: http://127.0.0.1:8000/health

## API Endpoints

### 1. Create Address
- **POST** `/addresses`
- **Description**: Create a new address entry
- **Request Body**:
  ```json
  {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "latitude": 40.7128,
    "longitude": -74.0060
  }
  ```

### 2. Get All Addresses
- **GET** `/addresses`
- **Description**: Retrieve all addresses (with pagination)
- **Query Parameters**:
  - `skip` (optional): Number of records to skip (default: 0)
  - `limit` (optional): Maximum number of records (default: 100, max: 1000)

### 3. Get Address by ID
- **GET** `/addresses/{address_id}`
- **Description**: Retrieve a specific address by its ID

### 4. Update Address
- **PUT** `/addresses/{address_id}`
- **Description**: Update an existing address (only provided fields will be updated)
- **Request Body** (all fields optional):
  ```json
  {
    "street": "456 Oak Ave",
    "city": "Los Angeles",
    "latitude": 34.0522,
    "longitude": -118.2437
  }
  ```

### 5. Delete Address
- **DELETE** `/addresses/{address_id}`
- **Description**: Delete an address by its ID

### 6. Search Addresses by Distance
- **POST** `/addresses/search`
- **Description**: Find all addresses within a specified distance from given coordinates
- **Request Body**:
  ```json
  {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "distance_km": 10.0
  }
  ```

## Example Usage

### Using cURL

**Create an address:**
```bash
curl -X POST "http://127.0.0.1:8000/addresses" \
  -H "Content-Type: application/json" \
  -d '{
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "latitude": 40.7128,
    "longitude": -74.0060
  }'
```

**Get all addresses:**
```bash
curl -X GET "http://127.0.0.1:8000/addresses"
```

**Search addresses within 10km:**
```bash
curl -X POST "http://127.0.0.1:8000/addresses/search" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 40.7128,
    "longitude": -74.0060,
    "distance_km": 10.0
  }'
```

### Using Python requests

```python
import requests

# Create an address
response = requests.post(
    "http://127.0.0.1:8000/addresses",
    json={
        "street": "123 Main St",
        "city": "New York",
        "state": "NY",
        "zip_code": "10001",
        "latitude": 40.7128,
        "longitude": -74.0060
    }
)
print(response.json())

# Search addresses within 10km
response = requests.post(
    "http://127.0.0.1:8000/addresses/search",
    json={
        "latitude": 40.7128,
        "longitude": -74.0060,
        "distance_km": 10.0
    }
)
print(response.json())
```

## Database

The application uses SQLite database (`address_book.db`) which is automatically created in the project root directory when the application starts.

The database schema includes:
- `id`: Primary key (auto-incrementing)
- `street`: Street address
- `city`: City name
- `state`: State/Province name
- `zip_code`: Postal/ZIP code
- `latitude`: Latitude coordinate (-90 to 90)
- `longitude`: Longitude coordinate (-180 to 180)

## Virtual Environment

This project uses a virtual environment to isolate dependencies. The virtual environment directory (`venv/`) is included in `.gitignore` and should not be committed to version control.

**To activate the virtual environment after initial setup:**

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

- **Windows (Command Prompt):**
  ```cmd
  venv\Scripts\activate.bat
  ```

- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

**To deactivate the virtual environment:**
```bash
deactivate
```

## Validation

The API includes comprehensive validation:

- **Required fields**: street, city, state, zip_code, latitude, longitude
- **Coordinate ranges**: 
  - Latitude: -90 to 90
  - Longitude: -180 to 180
- **String length limits**: Enforced for all text fields
- **Distance**: Must be positive (> 0) for search operations

## Logging

The application includes logging at various levels:
- **INFO**: General application flow and operations
- **DEBUG**: Detailed debugging information
- **WARNING**: Non-critical issues (e.g., resource not found)
- **ERROR**: Errors and exceptions

Logs are output to the console with timestamps and log levels.

## Testing the API

The easiest way to test the API is using the interactive Swagger UI:

1. Activate your virtual environment
2. Start the server: `uvicorn app.main:app --reload`
3. Open http://127.0.0.1:8000/docs in your browser
4. Use the "Try it out" feature to test each endpoint
5. View request/response schemas and examples

## Development Workflow

1. **Activate virtual environment** (if not already activated)
   ```bash
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Make changes** - The `--reload` flag will automatically restart the server when you save changes

4. **Test using Swagger UI** at http://127.0.0.1:8000/docs

## Best Practices Implemented

- ✅ Separation of concerns (models, schemas, CRUD, routes)
- ✅ Modular project structure with organized directories
- ✅ Virtual environment for dependency isolation
- ✅ Input validation using Pydantic
- ✅ Proper error handling and HTTP status codes
- ✅ Comprehensive logging
- ✅ Type hints throughout the codebase
- ✅ Docstrings and comments for documentation
- ✅ Database session management with dependencies
- ✅ RESTful API design principles
- ✅ Distance calculation using Haversine formula (accurate for Earth's surface)
- ✅ Router-based organization for scalability

## License

This project is created as a demonstration of FastAPI skills.
