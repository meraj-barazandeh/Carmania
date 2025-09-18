from flask import Blueprint, request, jsonify
from database import db
from models import Car, CarService, Customer
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

cars_bp = Blueprint("cars", __name__)


# Admin: Add Car
@cars_bp.route("/add", methods=["POST"])
@jwt_required()
def add_car():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "permission denied"}), 403

    data = request.get_json()
    owner_id = data.get("owner_id")
    make = data.get("make")
    model = data.get("model")
    year = data.get("year")

    owner = Customer.query.get(owner_id)
    if not owner:
        return jsonify({"error": "owner not found"}), 404

    car = Car(make=make, model=model, year=year, owner_id=owner.id)
    db.session.add(car)
    db.session.commit()

    return jsonify({"message": "car added", "car_id": car.id}), 201


#  Admin: Add Service
@cars_bp.route("/service", methods=["POST"])
@jwt_required()
def add_service():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "permission denied"}), 403

    data = request.get_json()
    car_id = data.get("car_id")
    mileage = data.get("mileage", 0)

    car = Car.query.get(car_id)
    if not car:
        return jsonify({"error": "car not found"}), 404

    service = CarService(
        car_id=car.id,
        mileage=mileage,
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

    return jsonify({"message": "service added", "service_id": service.id}), 201


#  Customer: List Own Cars + Last Service
@cars_bp.route("/my", methods=["GET"])
@jwt_required()
def list_my_cars():
    claims = get_jwt()
    if claims.get("role") != "customer":
        return jsonify({"error": "permission denied"}), 403

    user_id = int(get_jwt_identity())
    customer = Customer.query.get(user_id)
    if not customer:
        return jsonify({"error": "customer not found"}), 404

    cars_data = []
    for car in customer.cars:
        last_service = (
            CarService.query.filter_by(car_id=car.id)
            .order_by(CarService.mileage.desc())
            .first()
        )
        cars_data.append(
            {
                "id": car.id,
                "make": car.make,
                "model": car.model,
                "year": car.year,
                "last_service": (
                    {
                        "id": last_service.id if last_service else None,
                        "mileage": last_service.mileage if last_service else None,
                        "engine_oil": last_service.engine_oil if last_service else None,
                        "air_filter": last_service.air_filter if last_service else None,
                        "oil_filter": last_service.oil_filter if last_service else None,
                        "gear_oil": last_service.gear_oil if last_service else None,
                        "power_steering_oil": (
                            last_service.power_steering_oil if last_service else None
                        ),
                        "fuel_filter": (
                            last_service.fuel_filter if last_service else None
                        ),
                        "washer_fluid": (
                            last_service.washer_fluid if last_service else None
                        ),
                        "coolant": last_service.coolant if last_service else None,
                    }
                    if last_service
                    else None
                ),
            }
        )

    return jsonify({"cars": cars_data})
