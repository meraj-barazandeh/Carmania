from flask import request, Blueprint, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import Customer, Admin
from database import db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)


# CUSTOMER
@auth_bp.route("/customer/signup", methods=["POST"])
def customer_signup():
    data = request.get_json()
    phone = data.get("phone_number")
    email = data.get("email")
    password = data.get("password")

    if not phone or not email or not password:
        return jsonify({"error": "phone_number, email, and password required"}), 400

    if Customer.query.filter(
        (Customer.phone_number == phone) | (Customer.email == email)
    ).first():
        return jsonify({"error": "phone number or email already exists"}), 400

    hashed_password = generate_password_hash(password)
    customer = Customer(phone_number=phone, email=email, password=hashed_password)
    db.session.add(customer)
    db.session.commit()

    return jsonify({"message": "customer created successfully"}), 201


@auth_bp.route("/customer/login", methods=["POST"])
def customer_login():
    data = request.get_json()
    phone = data.get("phone_number")
    password = data.get("password")

    customer = Customer.query.filter_by(phone_number=phone).first()
    if not customer or not check_password_hash(customer.password, password):
        return jsonify({"error": "invalid phone_number or password"}), 401

    access_token = create_access_token(
        identity=str(customer.id), additional_claims={"role": "customer"}
    )

    return (
        jsonify(
            {
                "message": "login successful",
                "access_token": access_token,
                "role": "customer",
            }
        ),
        200,
    )


# ADMIn
@auth_bp.route("/admin/signup", methods=["POST"])
def admin_signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    if Admin.query.filter_by(username=username).first():
        return jsonify({"error": "username already exists"}), 400

    hashed_password = generate_password_hash(password)
    admin = Admin(username=username, password=hashed_password)
    db.session.add(admin)
    db.session.commit()

    return jsonify({"message": "admin created successfully"}), 201


@auth_bp.route("/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    admin = Admin.query.filter_by(username=username).first()
    if not admin or not check_password_hash(admin.password, password):
        return jsonify({"error": "invalid username or password"}), 401

    access_token = create_access_token(
        identity=str(admin.id), additional_claims={"role": "admin"}
    )

    return (
        jsonify(
            {
                "message": "login successful",
                "access_token": access_token,
                "role": "admin",
            }
        ),
        200,
    )
