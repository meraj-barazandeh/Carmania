from flask import Blueprint, request, jsonify
from database import db
from models import Car, CarService
from flask_jwt_extended import jwt_required, get_jwt

service_bp = Blueprint("service", __name__)


# Admin: Add Service by Car ID
@service_bp.route("/<int:car_id>", methods=["POST"])
@jwt_required()
def add_service(car_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "permission denied"}), 403

    car = Car.query.get(car_id)
    if not car:
        return jsonify({"error": "car not found"}), 404

    data = request.get_json() or {}

    service = CarService(
        car_id=car.id,
        mileage=data.get("mileage", 0),
        engine_oil=data.get("engine_oil", False),
        air_filter=data.get("air_filter", False),
        oil_filter=data.get("oil_filter", False),
        gear_oil=data.get("gear_oil", False),
        power_steering_oil=data.get("power_steering_oil", False),
        fuel_filter=data.get("fuel_filter", False),
        washer_fluid=data.get("washer_fluid", False),
        coolant=data.get("coolant", False),
    )

    db.session.add(service)
    db.session.commit()

    return jsonify({"message": "Service record added", "service_id": service.id}), 201
