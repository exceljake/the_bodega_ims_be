# schemas.py
from app import ma, db
from models import Product, Shop, User, Document, DocumentLine

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        fields = (
            "id",
            "name",
            "sku",
            "quantity",
            "price",
            "created_at",  
            "updated_at"
        )

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

class ShopSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Shop
        load_instance = True
        fields = (
            "id",
            "shop_name",
            "address",
            "contact_number",
            "created_at",  
            "updated_at"
        )

shop_schema = ShopSchema()
shops_schema = ShopSchema(many=True)
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
    
    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    role = ma.auto_field()
    shop_id = ma.auto_field()
    is_active = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class DocumentLineSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DocumentLine
        load_instance = True
    
    id = ma.auto_field()
    parent_document_id = ma.auto_field()
    quantity = ma.auto_field()
    product_id = ma.auto_field()
    price = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()

class DocumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Document
        load_instance = True
    
    id = ma.auto_field()
    document_type = ma.auto_field()
    total_quantity = ma.auto_field()
    received_by = ma.auto_field()
    delivered_by = ma.auto_field()
    supplier = ma.auto_field()
    document_date = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()
    
    # Include document lines in the response
    document_lines = ma.Nested(DocumentLineSchema, many=True, dump_only=True)

# Schema instances
document_line_schema = DocumentLineSchema()
document_lines_schema = DocumentLineSchema(many=True)
document_schema = DocumentSchema()
documents_schema = DocumentSchema(many=True)