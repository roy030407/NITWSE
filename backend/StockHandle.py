from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

structure = ['Name', 'Price', 'Owner', 'Supply']
app = Flask(__name__)
CORS(app)

# Use MongoDB Atlas URI (replace <db_password> with your actual password)
app.config["MONGO_URI"] = "mongodb+srv://nitwse:mayankthegoat@wse.0zosyhw.mongodb.net/nitwse?retryWrites=true&w=majority&appName=WSE"

mongo = PyMongo(app)

@app.route('/get_stocks', methods=['GET'])
def get_stocks():
    stocks = list(mongo.db.stockdata.find({}, {"_id": 0}))
    result = {}
    for stock in stocks:
        result[stock['Name']] = {
            "Name": stock['Name'],
            "Price": stock['Price']
        }
    return jsonify(result)

@app.route('/get_remaining_stocks', methods=['GET'])
def get_remaining_stocks():
    user_id = request.args.get('userID')
    if not user_id:
        return jsonify({"error": "userID is required"}), 400

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": "userID must be an integer"}), 400

    user_data = mongo.db.userdata.find_one({"userID": user_id}, {"_id": 0, "stocksOwned": 1})
    user_stocks = set(user_data.get("stocksOwned", {}).keys()) if user_data else set()

    all_stocks = list(mongo.db.stockdata.find({}, {"_id": 0}))
    remaining_stocks = [stock for stock in all_stocks if stock['Name'] not in user_stocks]

    return jsonify({"remaining_stocks": remaining_stocks})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
