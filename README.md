# CarMania

**CarMania** is a Flask-based REST API for managing car service centers and car sales. It allows admins and customers to manage cars, service records, and user accounts securely using **JWT authentication**.

## Features

* User management with **Admin** and **Customer** roles
* Add, view, and manage cars
* Record car services and maintenance history
* Secure authentication with JWT tokens
* Easily extendable for future functionality

## Project Structure

```
CarMania/
│
├─ app.py                  # Flask application entry point
├─ database.py             # SQLAlchemy database setup
├─ models.py               # Database models (Customer, Admin, Car, CarService)
├─ requirements.txt        # Python dependencies
├─ migrations/             # Alembic migrations folder
└─ routes/
   ├─ auth.py              # Signup/Login routes for users
   ├─ cars.py              # Car management routes
   └─ service.py           # Service records routes
```

## Installation

```bash
git clone https://github.com/meraj-barazandeh/Carmania.git
cd CarMania
python -m venv venv
source venv/bin/activate       # Linux / macOS
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

## Database Setup

```bash
export FLASK_APP=app:create_app   # Linux / macOS
set FLASK_APP=app:create_app      # Windows

flask db init        # Only the first time
flask db migrate -m "Initial migration"
flask db upgrade
```

## Running the Server

```bash
python app.py
```

Server runs at: `http://127.0.0.1:5000`

## Example API Requests

### Customer Signup & Login

```bash
curl -X POST http://127.0.0.1:5000/auth/customer/signup \
-H "Content-Type: application/json" \
-d '{"phone_number": "09123456789", "email": "test@example.com", "password": "123456"}'

curl -X POST http://127.0.0.1:5000/auth/customer/login \
-H "Content-Type: application/json" \
-d '{"phone_number": "09123456789", "password": "123456"}'
```

### Admin Signup & Login

```bash
curl -X POST http://127.0.0.1:5000/auth/admin/signup \
-H "Content-Type: application/json" \
-d '{"username": "admin1", "password": "123456"}'

curl -X POST http://127.0.0.1:5000/auth/admin/login \
-H "Content-Type: application/json" \
-d '{"username": "admin1", "password": "123456"}'
```

### Add Car (Admin)

```bash
curl -X POST http://127.0.0.1:5000/cars/add \
-H "Authorization: Bearer <JWT_TOKEN>" \
-H "Content-Type: application/json" \
-d '{"owner_id": 1, "make": "Peugeot", "model": "206", "year": 2018}'
```

### Add Service (Admin)

```bash
curl -X POST http://127.0.0.1:5000/cars/service \
-H "Authorization: Bearer <JWT_TOKEN>" \
-H "Content-Type: application/json" \
-d '{"car_id": 1, "mileage": 5000, "engine_oil": true, "air_filter": true}'
```

### List Customer Cars

```bash
curl -X GET http://127.0.0.1:5000/cars/my \
-H "Authorization: Bearer <JWT_TOKEN>"
```

## Security Notes

* Change **JWT\_SECRET\_KEY** in production
* Use HTTPS for production deployment
* Keep migrations in Git for consistent database state
