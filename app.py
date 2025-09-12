from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime
import requests
from functools import wraps

# Update the Flask app initialization to serve from parent directory
app = Flask(__name__, static_folder='..', static_url_path='')
CORS(app)

app.config["JWT_SECRET_KEY"] = "super-secret-key"  
jwt = JWTManager(app)

# Serve the home page
@app.route('/')
def serve_home():
    return send_from_directory(app.static_folder, 'new.html')

# ---------------- USERS ----------------
users = {
    "passenger1": {"password": "pass123", "role": "passenger"},
    "driver1": {"password": "driver123", "role": "driver"},
    "authority1": {"password": "auth123", "role": "authority"},
    "admin1": {"password": "admin123", "role": "admin"},
}

# Role-based access control decorator
def require_role(required_role):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            identity = get_jwt_identity()
            if identity["role"] != required_role:
                return jsonify({"msg": "Access forbidden - insufficient permissions"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ---------------- LOGIN ----------------
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username]["password"] == password:
        role = users[username]["role"]
        access_token = create_access_token(
            identity={"username": username, "role": role},
            expires_delta=datetime.timedelta(hours=3),
        )
        return jsonify(access_token=access_token, role=role, username=username)
    return jsonify({"msg": "Invalid username or password"}), 401

# ---------------- PASSENGER APIS ----------------
@app.route("/api/alerts", methods=["GET", "POST"])
@jwt_required()
def alerts():
    identity = get_jwt_identity()
    if request.method == "POST":
        msg = request.json.get("message", "")
        return jsonify({"msg": f"Alert '{msg}' created by {identity['username']}"})
    return jsonify([
        {"message": "Route A delayed", "time": "10:30 AM", "type": "delay"},
        {"message": "Bus 102 breakdown", "time": "11:15 AM", "type": "breakdown"}
    ])

@app.route("/api/buses", methods=["GET"])
@jwt_required()
def buses():
    return jsonify([
        {"id": "101", "route": "A", "lat": 22.7196, "lng": 75.8577, "eta": "5 min", "destination": "DAVV Campus"},
        {"id": "102", "route": "B", "lat": 22.7300, "lng": 75.8800, "eta": "12 min", "destination": "Rajwada"},
        {"id": "103", "route": "C", "lat": 22.7120, "lng": 75.8400, "eta": "8 min", "destination": "Railway Station"},
    ])

@app.route("/api/feedback", methods=["POST"])
@jwt_required()
def feedback():
    identity = get_jwt_identity()
    rating = request.json.get("rating", 5)
    comment = request.json.get("comment", "")
    return jsonify({"msg": f"Feedback submitted successfully by {identity['username']}", "rating": rating})

@app.route("/api/sos", methods=["POST"])
@jwt_required()
def sos():
    identity = get_jwt_identity()
    return jsonify({
        "msg": f"SOS triggered by {identity['username']}", 
        "location": request.json.get("location", "Unknown"),
        "timestamp": datetime.datetime.now().isoformat()
    })

# ---------------- DRIVER APIS ----------------
@app.route("/api/breakdown", methods=["POST"])
@require_role("driver")
def breakdown():
    identity = get_jwt_identity()
    location = request.json.get("location", "")
    issue = request.json.get("issue", "")
    details = request.json.get("details", "")
    return jsonify({
        "msg": f"Breakdown reported by driver {identity['username']}", 
        "location": location,
        "issue": issue,
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route("/api/driver/route-info", methods=["GET"])
@require_role("driver")
def driver_route_info():
    return jsonify({
        "current_route": "R102",
        "route_name": "Vijay Nagar to Railway Station",
        "stops": [
            {"name": "Vijay Nagar Square", "lat": 22.7276, "lng": 75.8723, "eta": "0 min"},
            {"name": "IT Park", "lat": 22.7196, "lng": 75.8577, "eta": "5 min"},
            {"name": "Geeta Bhawan", "lat": 22.7120, "lng": 75.8400, "eta": "15 min"},
            {"name": "Railway Station", "lat": 22.7050, "lng": 75.8350, "eta": "25 min"}
        ],
        "other_buses": [
            {"id": "101", "lat": 22.7276, "lng": 75.8723, "status": "On Time"},
            {"id": "103", "lat": 22.7120, "lng": 75.8400, "status": "Delayed"},
            {"id": "104", "lat": 22.7350, "lng": 75.8650, "status": "On Time"}
        ]
    })

@app.route("/api/chat/<route>", methods=["GET", "POST"])
@jwt_required()
def chat(route):
    identity = get_jwt_identity()
    if request.method == "POST":
        msg = request.json.get("message")
        return jsonify({
            "msg": f"Message sent on route {route}", 
            "user": identity['username'], 
            "message": msg,
            "timestamp": datetime.datetime.now().isoformat()
        })
    return jsonify([
        {"user": "driver1", "msg": "Any delays on this route?", "time": "10:30 AM"},
        {"user": "passenger1", "msg": "Just reached Geeta Bhawan stop", "time": "10:32 AM"}
    ])

# ---------------- AUTHORITY APIS ----------------
@app.route("/api/authority/all-vehicles", methods=["GET"])
@require_role("authority")
def get_all_vehicles():
    return jsonify([
        {"id": "BUS101", "type": "driver", "location": {"lat": 22.7196, "lng": 75.8577}, "status": "Active", "route": "R102"},
        {"id": "BUS102", "type": "driver", "location": {"lat": 22.7276, "lng": 75.8723}, "status": "Active", "route": "R101"},
        {"id": "BUS103", "type": "driver", "location": {"lat": 22.7120, "lng": 75.8400}, "status": "Maintenance", "route": "R103"},
        {"id": "PASS101", "type": "passenger", "location": {"lat": 22.7120, "lng": 75.8400}, "status": "Waiting", "route": "R102"}
    ])

@app.route("/api/authority/analytics", methods=["GET"])
@require_role("authority")
def get_authority_analytics():
    return jsonify({
        "total_active_buses": 25,
        "total_passengers": 150,
        "emergency_alerts": 2,
        "route_delays": 3,
        "buses_in_maintenance": 3,
        "average_delay_time": "5 mins"
    })

@app.route("/api/monitor", methods=["GET"])
@require_role("authority")
def monitor():
    return jsonify({
        "ratings_count": {"5": 45, "4": 23, "3": 12, "2": 5, "1": 2},
        "breakdowns": [
            {"issue": "Engine", "count": 2, "severity": "High"},
            {"issue": "Flat Tire", "count": 1, "severity": "Medium"},
            {"issue": "AC Problem", "count": 3, "severity": "Low"}
        ],
        "sos_logs": [
            {"driver": "driver1", "active": 0, "last_triggered": "Never"},
            {"passenger": "passenger1", "active": 1, "last_triggered": "10:45 AM"}
        ],
    })

# ---------------- ADMIN APIS ----------------
@app.route("/api/admin/users", methods=["GET"])
@require_role("admin")
def admin_users():
    return jsonify([
        {"username": u, "role": users[u]["role"], "status": "Active"} for u in users
    ])

@app.route("/api/admin/system", methods=["GET"])
@require_role("admin")
def admin_system():
    return jsonify({
        "uptime": "99.9%",
        "active_users": 120,
        "buses_in_service": 34,
        "total_routes": 12,
        "server_status": "Healthy",
        "database_status": "Connected"
    })

@app.route("/api/admin/add-user", methods=["POST"])
@require_role("admin")
def admin_add_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")
    
    if username in users:
        return jsonify({"msg": "User already exists"}), 400
    
    users[username] = {"password": password, "role": role}
    return jsonify({"msg": f"User {username} added successfully"})

# ---------------- USER PROFILE ----------------
@app.route("/api/profile", methods=["GET"])
@jwt_required()
def get_profile():
    identity = get_jwt_identity()
    return jsonify({
        "username": identity["username"],
        "role": identity["role"],
        "login_time": datetime.datetime.now().isoformat()
    })

# ---------------- LOGOUT ----------------
@app.route("/api/logout", methods=["POST"])
@jwt_required()
def logout():
    # In a real application, you might want to blacklist the token
    return jsonify({"msg": "Logout successful"})

# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)