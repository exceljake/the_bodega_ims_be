# resources.py
from flask import request
from flask_restful import Resource
from app import db
from models import Product, Shop, User, Document, DocumentLine
from schemas import product_schema, products_schema, shop_schema, shops_schema, user_schema, users_schema, document_schema, documents_schema, document_line_schema, document_lines_schema
from datetime import datetime

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
        new_shop.create_default_users()
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
    
class UserLoginResource(Resource):
    def post(self):
        data = request.json
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            return {"message": "Username and password required"}, 400
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            return {
                "message": "Login successful",
                "user": user_schema.dump(user)
            }, 200
        
        return {"message": "Invalid credentials"}, 401

class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)

class UserResource(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        return user_schema.dump(user)

class DocumentListResource(Resource):
    def get(self):
        documents = Document.query.all()
        return documents_schema.dump(documents)
    
    def post(self):
        data = request.json
        
        # Validation
        if data["document_type"] not in ["in", "out"]:
            return {"message": "Document type must be 'in' or 'out'"}, 422
        
        if not data.get("document_lines") or len(data["document_lines"]) == 0:
            return {"message": "Document must have at least one line"}, 422
        
        # Parse document_date
        try:
            document_date = datetime.strptime(data["document_date"], "%Y-%m-%d").date()
        except ValueError:
            return {"message": "Invalid document_date format. Use YYYY-MM-DD"}, 422
        
        # Create document
        new_document = Document(
            document_type=data["document_type"],
            total_quantity=data.get("total_quantity", 0.0),
            received_by=data["received_by"],
            delivered_by=data["delivered_by"],
            supplier=data["supplier"],
            document_date=document_date
        )
        
        db.session.add(new_document)
        db.session.commit()  # Commit to get document ID
        
        # Create document lines
        for line_data in data["document_lines"]:
            # Check if product exists
            product = Product.query.get(line_data["product_id"])
            if not product:
                return {"message": f"Product with ID {line_data['product_id']} not found"}, 422
            
            # Check if sufficient quantity for 'out' documents
            if data["document_type"] == "out" and product.quantity < line_data["quantity"]:
                return {"message": f"Insufficient quantity for product {product.name}. Available: {product.quantity}, Required: {line_data['quantity']}"}, 422
            
            new_line = DocumentLine(
                parent_document_id=new_document.id,
                quantity=line_data["quantity"],
                product_id=line_data["product_id"],
                price=line_data.get("price", 0.0)
            )
            db.session.add(new_line)
        
        db.session.commit()
        
        # Update product quantities
        new_document.update_product_quantities()
        
        return document_schema.dump(new_document), 201

class DocumentResource(Resource):
    def get(self, id):
        document = Document.query.get_or_404(id)
        return document_schema.dump(document)
    
    def delete(self, id):
        document = Document.query.get_or_404(id)
        
        # Reverse the quantity changes before deleting
        for line in document.document_lines:
            product = Product.query.get(line.product_id)
            if product:
                if document.document_type == 'in':
                    # Reverse the addition by subtracting
                    product.quantity -= line.quantity
                elif document.document_type == 'out':
                    # Reverse the subtraction by adding
                    product.quantity += line.quantity
        
        db.session.delete(document)  # This will also delete document_lines due to cascade
        db.session.commit()
        
        return {"message": "Document deleted successfully"}, 200
    
    
    
    
    

    
