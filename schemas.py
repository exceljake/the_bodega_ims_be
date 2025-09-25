# schemas.py
from app import ma, db
from models import Product, Shop, User

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