from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MongoDB Atlas URI (replace <db_password> with your actual password)
app.config["MONGO_URI"] = "mongodb+srv://nitwse:mayankthegoat@wse.0zosyhw.mongodb.net/nitwse?retryWrites=true&w=majority&appName=WSE"

mongo = PyMongo(app)

def updateBalance(userID, updatedPrice):
    temp = mongo.db.usertransactions.find_one({"userID": userID})
    if temp["balance"] + updatedPrice < 0:
        return False
    else:
        mongo.db.usertransactions.update_one(
            {"userID": userID},
            {"$inc": {"balance": updatedPrice}}
        )
        return True

def buyStock(userID, stockPrice, quantity, stockName):
    if updateBalance(userID, -1 * stockPrice * quantity):
        mongo.db.usertransactions.update_one(
            {"userID": userID},
            {"$inc": {f"stocksOwned.{stockName}": quantity}}
        )
        return True
    return False

def sellStock(userID, stockPrice, quantity, stockName):
    temp = mongo.db.usertransactions.find_one({"userID": userID})
    if stockName in temp["stocksOwned"] and temp["stocksOwned"][stockName] >= quantity:
        mongo.db.usertransactions.update_one(
            {"userID": userID},
            {"$inc": {f"stocksOwned.{stockName}": -quantity}}
        )
        updateBalance(userID, stockPrice * quantity)
        return True
    else:
        return False

@app.route('/buy', methods=['POST'])
def buy():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON received"}), 400

    userID = int(data["userID"])
    stockPrice = float(data["stockPrice"])
    quantity = int(data["quantity"])
    stockName = data["stockName"]

    result = mongo.db.usertransactions.update_one(
        {
            "userID": userID,
            "balance": {"$gte": stockPrice * quantity}
        },
        {
            "$inc": {
                "balance": -stockPrice * quantity,
                f"stocksOwned.{stockName}": quantity
            }
        }
    )

    if result.modified_count == 1:
        return jsonify({"status": "success", "message": "Transaction Successful"})
    else:
        return jsonify({"status": "failed", "message": "Invalid Transaction or Insufficient balance"})

@app.route('/sell', methods=['POST'])
def sell():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON received"}), 400

    required_keys = ["userID", "stockPrice", "quantity", "stockName"]
    for key in required_keys:
        if key not in data:
            return jsonify({"status": "error", "message": f"Missing key: {key}"}), 400

    try:
        userID = int(data["userID"])
        stockPrice = float(data["stockPrice"])
        quantity = int(data["quantity"])
        stockName = data["stockName"]
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid data types"}), 400

    if quantity <= 0 or stockPrice <= 0:
        return jsonify({"status": "error", "message": "Quantity and stockPrice must be positive"}), 400

    if sellStock(userID, stockPrice, quantity, stockName):
        return jsonify({"status": "success", "message": "Transaction Successful"})
    else:
        return jsonify({"status": "failed", "message": "Invalid Transaction"})

@app.route('/import', methods=['GET'])
def display():
    userID = int(request.args.get("userID"))
    user = mongo.db.usertransactions.find_one({"userID": userID})
    if user:
        return jsonify({
            "balance": user["balance"],
            "stocks": user["stocksOwned"]
        })
    else:
        return jsonify({
            "error": "User not found",
            "stocks": {}
        }), 404

if __name__ == "__main__":
    app.run(debug=True)
