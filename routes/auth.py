from flask import request, Blueprint, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from database import db

auth_bp = Blueprint("auth", __name__)
