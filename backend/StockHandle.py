from flask import request, jsonify
from flask_pymongo import PyMongo

structure = ['Name', 'Price', 'Owner', 'Supply']

def get_stocks(mongo):
    stocks = list(mongo.db.stockdata.find({}, {"_id": 0}))
    result = {}
    for stock in stocks:
        result[stock['Name']] = {
            "Name": stock['Name'],
            "Price": stock['Price']
        }
    return jsonify(result)

def get_remaining_stocks(mongo):
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
