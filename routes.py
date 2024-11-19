from flask import request, jsonify
from schemas import Vehicle, SoldVehicles
from database import db

def init_routes(app):
    @app.route('/vehicle', methods=['GET'])
    def get_vehicles():
        """
        Get all vehicles
        ---
        responses:
          200:
            description: List of vehicles
            schema:
              type: array
              items:
                type: object
                properties:
                  manufacturer_name:
                    type: string
                  description:
                    type: string
                  horse_power:
                    type: integer
                  model_name:
                    type: string
                  model_year:
                    type: integer
                  purchase_price:
                    type: number
                  fuel_type:
                    type: string
                  vin_number:
                    type: string
        """
        vehicles = Vehicle.query.all()
        vehicle_list = []
        for vehicle in vehicles:
            vehicle_dict = vehicle.to_dictionary()
            vehicle_list.append(vehicle_dict)

        return jsonify(vehicle_list), 200

    @app.route('/vehicle', methods=['POST'])
    def add_vehicle():
        """
        Add new vehicle
        ---
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - manufacturer_name
                - horse_power
                - model_name
                - model_year
                - purchase_price
                - fuel_type
                - vin_number
              properties:
                manufacturer_name:
                  type: string
                description:
                  type: string
                horse_power:
                  type: integer
                model_name:
                  type: string
                model_year:
                  type: integer
                purchase_price:
                  type: number
                fuel_type:
                  type: string
                vin_number:
                  type: string
        responses:
          201:
            description: Vehicle created successfully
          422:
            description: Missing or invalid data
        """
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
                vin_number=data['vin_number'].lower(),
                color = data['color'],
                vehicle_type=data['vehicle_type']
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
        """
        Get vehicle by VIN
        ---
        parameters:
          - in: path
            name: vin
            required: true
            type: string
        responses:
          200:
            description: Vehicle found
          404:
            description: Vehicle not found
        """
        vehicle = Vehicle.query.filter_by(vin_number=vin.lower()).first()
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404
        return jsonify(vehicle.to_dictionary()), 200

    @app.route('/vehicle/<string:vin>', methods=['PUT'])
    def update_vehicle(vin):
        """
        Update vehicle by VIN
        ---
        parameters:
          - in: path
            name: vin
            required: true
            type: string
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                manufacturer_name:
                  type: string
                description:
                  type: string
                horse_power:
                  type: integer
                model_name:
                  type: string
                model_year:
                  type: integer
                purchase_price:
                  type: number
                fuel_type:
                  type: string
        responses:
          200:
            description: Vehicle updated successfully
          404:
            description: Vehicle not found
          422:
            description: Missing or invalid data
        """
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
            vehicle.color = data['color']
            vehicle.vehicle_type = data['vehicle_type']
            db.session.commit()
            return jsonify(vehicle.to_dictionary()), 200
        except KeyError as e:
            return jsonify({"error": f"Missing or invalid key: {e}"}), 422
        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}"}), 422

    @app.route('/vehicle/<string:vin>', methods=['DELETE'])
    def delete_vehicle(vin):
        """
        Delete vehicle by VIN
        ---
        parameters:
          - in: path
            name: vin
            required: true
            type: string
        responses:
          204:
            description: Vehicle deleted successfully
          404:
            description: Vehicle not found
        """
        vehicle = Vehicle.query.filter_by(vin_number=vin.lower()).first()
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404

        db.session.delete(vehicle)
        db.session.commit()
        return '', 204

    @app.route('/sold-vehicles', methods=['GET'])
    def get_sold_vehicles():
        vehicles = Vehicle.query.all()
        sold_vehicles = SoldVehicles.query.all()
        vin_numbers = set()
        for i in vehicles:
            vin_numbers.add(i.vin_number)
        
        sold = []
        for i in sold_vehicles:
            if i.vin in vin_numbers:
                sold.append(i)

        return sold
                
                
