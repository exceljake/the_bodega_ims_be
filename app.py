from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
import os
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()

# --- Initialize app ---
app = Flask(__name__)

# --- Config (MySQL) ---
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root@localhost/the_bodega_development"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# --- Extensions ---
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

# --- Model ---
class Product(db.Model):
    __tablename__ = "products"   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False, default=0.0)

# --- Schema ---
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# --- Resources ---
class ProductListResource(Resource):
    def get(self):
        products = Product.query.all()
        return products_schema.dump(products)

    def post(self):
        data = request.json
        new_product = Product(
            name=data["name"],
            sku=data["sku"],
            quantity=data["quantity"],
            price=data["price"]
        )
        db.session.add(new_product)
        db.session.commit()
        return product_schema.dump(new_product), 201

class ProductResource(Resource):
    def get(self, id):
        product = Product.query.get_or_404(id)
        return product_schema.dump(product)

    def put(self, id):
        product = Product.query.get_or_404(id)
        data = request.json
        for key, value in data.items():
            setattr(product, key, value)
        db.session.commit()
        return product_schema.dump(product)

    def delete(self, id):
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted successfully"}, 204

# --- Register Routes ---
api.add_resource(ProductListResource, "/products")
api.add_resource(ProductResource, "/products/<int:id>")

# --- Bootstrap ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("✅ Registered routes:", app.url_map)
    app.run(debug=True)