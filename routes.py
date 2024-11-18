from flask import request, jsonify
from schemas import Vehicle
from database import db

def init_routes(app):
    @app.route('/vehicle', methods=['GET'])
    def get_vehicles():
        # get all vehicles
        return jsonify([]), 200

    @app.route('/vehicle', methods=['POST'])
    def add_vehicle():
        # add new vehicle
        return jsonify({"message": "Vehicle added"}), 201

    @app.route('/vehicle/<string:vin>', methods=['GET'])
    def get_vehicle(vin):
        # get vehicle by vin
        return jsonify({"message": f"Vehicle {vin} found"}), 200

    @app.route('/vehicle/<string:vin>', methods=['PUT'])
    def update_vehicle(vin):
        # update vehicle by vin
        return jsonify({"message": f"Vehicle {vin} updated"}), 200

    @app.route('/vehicle/<string:vin>', methods=['DELETE'])
    def delete_vehicle(vin):
        # delete vehicle by vin
        return '', 204
