from flask import Flask
from flask_cors import CORS # Ensure this is here
from app.database import db
from app.routes import setup_routes

app = Flask(__name__)

# Ye line frontend connection ke liye sabse zaroori hai
CORS(app, resources={r"/api/*": {"origins": "*"}}) 

setup_routes(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)