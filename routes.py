from flask import request, jsonify
from schemas import Vehicle
from database import db

def init_routes(app):
    @app.route('/vehicle', methods=['GET'])
    def get_vehicles():
        # get all vehicles
        vehicles = Vehicle.query.all()
        vehicle_list = []
        for vehicle in vehicles:
            vehicle_dict = vehicle.to_dictionary()
            vehicle_list.append(vehicle_dict)

        return jsonify(vehicle_list), 200

    @app.route('/vehicle', methods=['POST'])
    def add_vehicle():
        # add new vehicle
        try:
            data = request.get_json()
            vehicle = Vehicle(
                manufacturer_name=data['manufacturer_name'],
                description=data.get('description', ''),
                horse_power=data['horse_power'],
                model_name=data['model_name'],
                model_year=data['model_year'],
                purchase_price=data['purchase_price'],
                fuel_type=data['fuel_type'],
                vin_number=data['vin_number'].lower()
            )
            db.session.add(vehicle)
            db.session.commit()
            return jsonify(vehicle.to_dictionary()), 201
        except KeyError as e:
            db.session.rollback()
            return jsonify({"error": f"Missing or invalid key: {e}"}), 422
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"An error occurred: {e}"}), 422

    @app.route('/vehicle/<string:vin>', methods=['GET'])
    def get_vehicle(vin):
        # get vehicle by vin
        vehicle = Vehicle.query.filter_by(vin_number=vin.lower()).first()
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404
        return jsonify(vehicle.to_dictionary()), 200

    @app.route('/vehicle/<string:vin>', methods=['PUT'])
    def update_vehicle(vin):
        # update vehicle by vin
        vehicle = Vehicle.query.filter_by(vin_number=vin.lower()).first()
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404

        try:
            data = request.get_json()
            vehicle.manufacturer_name = data['manufacturer_name']
            vehicle.description = data.get('description', vehicle.description)
            vehicle.horse_power = data['horse_power']
            vehicle.model_name = data['model_name']
            vehicle.model_year = data['model_year']
            vehicle.purchase_price = data['purchase_price']
            vehicle.fuel_type = data['fuel_type']
            db.session.commit()
            return jsonify(vehicle.to_dictionary()), 200
        except KeyError as e:
            return jsonify({"error": f"Missing or invalid key: {e}"}), 422
        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}"}), 422

    @app.route('/vehicle/<string:vin>', methods=['DELETE'])
    def delete_vehicle(vin):
        # delete vehicle by vin
        vehicle = Vehicle.query.filter_by(vin_number=vin.lower()).first()
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404

        db.session.delete(vehicle)
        db.session.commit()
        return '', 204
