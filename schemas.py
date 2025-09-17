# schemas.py
from app import ma
from models import Product

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