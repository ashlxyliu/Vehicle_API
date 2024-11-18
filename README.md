# Vehicle API

This project is a Flask web service that provides CRUD operations for vehicle data, complete with test cases.

# Features
- RESTful API: CRUD operations for managing vehicle data.
- Database Integration: Uses SQLAlchemy with an SQLite database.
- Swagger: Integrated API documentation for easy interaction/testing.
- Error Handling: Comprehensive error handling for missing/invalid data.
- Test Suite: Comprehensive test suite for routes and data validation using 
pytest.

# Technologies Used
- Python
- Flask
- Flask-SQLAlchemy
- Flasgger
- SQLite
- Pytest

# Installation
1. Clone the repository.
  git clone https://github.com/yourusername/vehicleapi.git
  cd vehicleapi
  
2. Set up virtual environment.
  python3 -m venv venv
  source venv/bin/activate  # On Unix/macOS
  venv\Scripts\activate  # On Windows

3. Install dependencies.
  pip install -r requirements.txt

# Run Flask application
python app.py

Visit http://127.0.0.1:5000/ to check the home route message.

Visit http://127.0.0.1:5000/apidocs/ to access the Swagger UI for interactive API documentation. Swagger provides detailed information on each endpoint, including request parameters and example responses.

# Run test suite
pytest tests.py

# Endpoints
1. Get All Vehicles
  Method: GET
  Endpoint: /vehicle
  Response: 200 OK with a list of all vehicles.

2. Add a New Vehicle
  Method: POST
  Endpoint: /vehicle
  Request Body:
  {
    "vin_number": "1hgcm82633a123456",
    "manufacturer_name": "Honda",
    "description": "A reliable car",
    "horse_power": 200,
    "model_name": "Accord",
    "model_year": 2022,
    "purchase_price": 25000.00,
    "fuel_type": "Gasoline"
  }
  Response: 201 Created with the newly added vehicle details.

3. Get Vehicle by VIN
  Method: GET
  Endpoint: /vehicle/{vin}
  Response: 200 OK with vehicle details or 404 Not Found.

4. Update Vehicle by VIN
  Method: PUT
  Endpoint: /vehicle/{vin}
  Request Body:
  {
    "manufacturer_name": "Updated Honda",
    "description": "Updated description",
    "horse_power": 210,
    "model_name": "Accord",
    "model_year": 2023,
    "purchase_price": 26000.00,
    "fuel_type": "Gasoline"
  }
  Response: 200 OK with updated vehicle details or 404 Not Found.

5. Delete Vehicle by VIN
  Method: DELETE
  Endpoint: /vehicle/{vin}
  Response: 204 No Content or 404 Not Found.


