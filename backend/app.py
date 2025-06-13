from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import os
from dotenv import load_dotenv
import sys

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB configuration
app.config["MONGO_URI"] = os.getenv("MONGODB_URI", "mongodb+srv://nitwse:mayankthegoat@wse.0zosyhw.mongodb.net/nitwse?retryWrites=true&w=majority&appName=WSE")
mongo = PyMongo(app)

# Import all routes
from backend.LoginHandle import signup, login
from backend.StockHandle import get_stocks, get_remaining_stocks
from backend.TransactionHandle import buy, sell, display

# Register all routes
app.add_url_rule('/signup', 'signup', lambda: signup(), methods=['POST'])
app.add_url_rule('/login', 'login', lambda: login(), methods=['POST'])
app.add_url_rule('/get_stocks', 'get_stocks', lambda: get_stocks(mongo), methods=['GET'])
app.add_url_rule('/get_remaining_stocks', 'get_remaining_stocks', lambda: get_remaining_stocks(mongo), methods=['GET'])
app.add_url_rule('/buy', 'buy', lambda: buy(mongo), methods=['POST'])
app.add_url_rule('/sell', 'sell', lambda: sell(mongo), methods=['POST'])
app.add_url_rule('/import', 'display', lambda: display(mongo), methods=['GET'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 10000))) 
