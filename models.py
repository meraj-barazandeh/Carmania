# models.py
from database import db


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    cars = db.relationship("Car", back_populates="owner", cascade="all, delete-orphan")


class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Car(db.Model):
    __tablename__ = "cars"

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=True)

    owner_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    owner = db.relationship("Customer", back_populates="cars")

    service_records = db.relationship(
        "CarService",
        back_populates="car",
        cascade="all, delete-orphan",
        order_by="CarService.mileage.desc()",
    )


class CarService(db.Model):
    __tablename__ = "car_services"

    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey("cars.id"), nullable=False)

    engine_oil = db.Column(db.Boolean, default=False)
    air_filter = db.Column(db.Boolean, default=False)
    oil_filter = db.Column(db.Boolean, default=False)
    gear_oil = db.Column(db.Boolean, default=False)
    power_steering_oil = db.Column(db.Boolean, default=False)
    fuel_filter = db.Column(db.Boolean, default=False)
    washer_fluid = db.Column(db.Boolean, default=False)
    coolant = db.Column(db.Boolean, default=False)

    mileage = db.Column(db.Integer, nullable=False)

    car = db.relationship("Car", back_populates="service_records")
