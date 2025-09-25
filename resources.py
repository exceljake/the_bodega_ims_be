# resources.py
from flask import request
from flask_restful import Resource
from app import db
from models import Product, Shop
from schemas import product_schema, products_schema, shop_schema, shops_schema

class ProductListResource(Resource):
    def get(self):
        products = Product.query.all()
        return products_schema.dump(products)

    def post(self):
        data = request.json
        existing_sku = Product.query.filter_by(sku=data["sku"]).first()
        existing_name = Product.query.filter_by(name=data["name"]).first()
        if existing_sku:
            return {"message": "SKU already existing"}, 422
        if existing_name:
            return {"message": "Name already existing"}, 422
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
    
class ShopListResource(Resource):
    def get(self):
        shops = Shop.query.all()
        return shops_schema.dump(shops)
    
    def post(self):
        data = request.json
        existing_name = Shop.query.filter_by(shop_name=data["shop_name"]).first()
        if existing_name:
            return {"message": "Shop name already existing"}, 422
        new_shop = Shop(
            shop_name=data["shop_name"],
            address=data["address"],
            contact_number=data["contact_number"]
        )
        db.session.add(new_shop)
        db.session.commit()
        return shop_schema.dump(new_shop), 201
    
class ShopResource(Resource):
    def get(self, id):
        shop = Shop.query.get_or_404(id)
        return shop_schema.dump(shop)

    def put(self, id):
        shop = Shop.query.get_or_404(id)
        data = request.json
        for key, value in data.items():
            setattr(shop, key, value)
        db.session.commit()
        return shop_schema.dump(shop)

    def delete(self, id):
        shop = Shop.query.get_or_404(id)
        db.session.delete(shop)
        db.session.commit()
        return {"message": "Shop deleted successfully"}, 204