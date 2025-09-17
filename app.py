from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_cors import CORS
import os
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()

# --- Initialize app ---
app = Flask(__name__)

# --- Enable CORS ---
CORS(app)

# --- Config (MySQL) ---
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

# --- Extensions ---
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

# --- Import Models and Schemas ---
from models import Product
from schemas import product_schema, products_schema

# --- Import Resources ---
from resources import ProductListResource, ProductResource

# --- Register Routes ---
api.add_resource(ProductListResource, "/products")
api.add_resource(ProductResource, "/products/<int:id>")

# --- Bootstrap ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("✅ Registered routes:", app.url_map)