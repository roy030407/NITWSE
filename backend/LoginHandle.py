from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Connect to MongoDB Atlas (replace <db_password> with your actual password)
client = MongoClient("mongodb+srv://nitwse:mayankthegoat@wse.0zosyhw.mongodb.net/?retryWrites=true&w=majority&appName=WSE")
db = client["nitwse"]
users = db["users"]

def get_next_user_id():
    # Find the highest user ID
    highest_user = users.find_one(sort=[("userId", -1)])
    if highest_user and "userId" in highest_user:
        return highest_user["userId"] + 1
    return 1001  # Start from 1001 if no users exist

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if users.find_one({"email": email}):
        return jsonify({"message": "User already exists", "success": False}), 409

    # Generate new user ID
    userId = get_next_user_id()

    # Insert user with the generated ID
    users.insert_one({
        "name": name,
        "email": email,
        "password": password,
        "userId": userId
    })
    
    return jsonify({
        "message": "Signup successful",
        "success": True,
        "userId": userId,
        "name": name
    }), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = users.find_one({"email": email, "password": password})
    if user:
        return jsonify({
            "message": "Login successful",
            "success": True,
            "userId": user["userId"],
            "name": user["name"]
        }), 200
    return jsonify({"message": "Invalid credentials", "success": False}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5002)