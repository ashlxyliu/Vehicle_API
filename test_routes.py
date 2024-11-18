import pytest
from app import app, db, Vehicle

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()  

@pytest.fixture
def sample_data():
    with app.app_context():
        db.session.query(Vehicle).delete()  
        vehicle1 = Vehicle(
            manufacturer_name = "Audi",
            description = "Firmament Blue metallic",
            horse_power = 335,
            model_name = "A8",
            model_year = 2024,
            purchase_price = 92000.00,
            fuel_type = "Gasoline",
            vin_number = "1hgcm82633a123456"
        )
        vehicle2 = Vehicle(
            manufacturer_name = "Volvo",
            description = "Silver Dawn",
            horse_power = 455,
            model_name = "XC90",
            model_year = 2024,
            purchase_price = 71000.00,
            fuel_type = "Hybrid",
            vin_number = "1ftfw1et1ef123456"
        )
        db.session.add_all([vehicle1, vehicle2])
        db.session.commit()

def test_get_vehicles(client, sample_data):
    response = client.get('/vehicle')
    assert response.status_code == 200
    assert len(response.get_json()) == 2
    assert response.get_json()[0]['manufacturer_name'] == "Audi"
    assert response.get_json()[1]['model_name'] == "XC90"

def test_add_vehicle(client):
    data = {
        "manufacturer_name": "Jeep",
        "description": "Bright White",
        "horse_power": 430,
        "model_name": "Wrangler",
        "model_year": 2024,
        "purchase_price": 50000.00,
        "fuel_type": "Hybrid",
        "vin_number": "2hgcm82633a654321"
    }
    response = client.post('/vehicle', json=data)
    assert response.status_code == 201
    assert response.get_json()['manufacturer_name'] == "Jeep"
    assert response.get_json()['vin_number'] == "2hgcm82633a654321"

def test_get_vehicle(client, sample_data):
    response = client.get('/vehicle/1hgcm82633a123456')
    assert response.status_code == 200
    assert response.get_json()['model_name'] == "A8"
    assert response.get_json()['fuel_type'] == "Gasoline"

def test_update_vehicle(client, sample_data):
    updated_data = {
        "manufacturer_name": "Audi",
        "description": "Glacier White metallic",
        "horse_power": 335,
        "model_name": "A8",
        "model_year": 2022,
        "purchase_price": 92000.00,
        "fuel_type": "Gasoline"
    }
    response = client.put('/vehicle/1hgcm82633a123456', json=updated_data)
    assert response.status_code == 200
    assert response.get_json()['model_year'] == 2022
    assert response.get_json()['description'] == "Glacier White metallic"

def test_delete_vehicle(client, sample_data):
    response = client.delete('/vehicle/1hgcm82633a123456')
    assert response.status_code == 204
    response = client.get('/vehicle/1hgcm82633a123456')
    assert response.status_code == 404

def test_add_vehicle_with_missing_required_field(client):
    data = {
        "description": "Solid Black",
        "horse_power": 300,
        "model_name": "Model 3",
        "model_year": 2024,
        "purchase_price": 31000.00,
        "fuel_type": "Electric",
        "vin_number": "5npdh4ae3gh123456"
    }
    response = client.post('/vehicle', json=data)
    assert response.status_code == 422
    assert "error" in response.get_json()

def test_add_vehicle_with_invalid_field_types(client):
    data = {
        "manufacturer_name": "Hyundai",
        "description": "Invalid horse_power type",
        "horse_power": "one hundred twenty",
        "model_name": "Accent",
        "model_year": "twenty twenty-three", 
        "purchase_price": "not a number", 
        "fuel_type": "Gasoline",
        "vin_number": "5npdh4ae3gh789012"
    }
    response = client.post('/vehicle', json=data)
    assert response.status_code == 422
    assert "error" in response.get_json()

def test_case_insensitive_vin(client, sample_data):
    response = client.get('/vehicle/1FTFW1ET1EF123456'.lower()) 
    assert response.status_code == 200
    assert response.get_json()['model_name'] == "XC90"

def test_add_vehicle_with_existing_vin_different_case(client, sample_data):
    data = {
        "manufacturer_name": "Volvo",
        "description": "Duplicate VIN but with different case",
        "horse_power": 300,
        "model_name": "Duplicate Test",
        "model_year": 2022,
        "purchase_price": 30000.00,
        "fuel_type": "Gasoline",
        "vin_number": "1FTFW1ET1EF123456".upper()  # different case
    }
    response = client.post('/vehicle', json=data)
    assert response.status_code == 422
    assert "error" in response.get_json()

def test_get_vehicles_empty_database(client):
    # empty database
    response = client.get('/vehicle')
    assert response.status_code == 200
    assert response.get_json() == [] 

def test_update_vehicle_with_invalid_field_types(client, sample_data):
    # invalid field types
    invalid_data = {
        "manufacturer_name": "Audi",
        "description": "Firmament Blue metallic",
        "horse_power": "fast",  # invalid type
        "model_name": "A8",
        "model_year": "recent",  # invalid type
        "purchase_price": "expensive",  # invalid type
        "fuel_type": "Gasoline"
    }
    response = client.put('/vehicle/1hgcm82633a123456', json=invalid_data)
    assert response.status_code == 422
    assert "error" in response.get_json()

def test_update_non_existent_vehicle(client):
    update_data = {
        "manufacturer_name": "Unknown",
        "description": "Non-existent vehicle update",
        "horse_power": 200,
        "model_name": "Unknown Model",
        "model_year": 2021,
        "purchase_price": 5000.00,
        "fuel_type": "Gasoline"
    }
    response = client.put('/vehicle/0abcdef1234567890', json=update_data)  # non-existent vin
    assert response.status_code == 404
    assert response.get_json()['error'] == "Vehicle not found"

def test_delete_vehicle_twice(client, sample_data):
    response = client.delete('/vehicle/1hgcm82633a123456')
    assert response.status_code == 204
    response = client.delete('/vehicle/1hgcm82633a123456')
    assert response.status_code == 404
    assert response.get_json()['error'] == "Vehicle not found"

