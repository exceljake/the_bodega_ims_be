# schemas.py
from app import ma
from models import Product, Shop

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