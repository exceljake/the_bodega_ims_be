from app import db

class Product(db.Model):
    __tablename__ = "products"   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False, default=0.0)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    shop = db.relationship('Shop', backref=db.backref('products', lazy=True))
    
class Shop(db.Model):
    __tablename__ = 'shops'
    id = db.Column(db.Integer, primary_key=True)
    shop_name = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.Text)
    contact_number = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    def create_default_users(self):
        from app import db

        owner = User(
            username=f"{self.shop_name.lower().replace(' ', '_')}_owner",
            email=f"owner@{self.shop_name.lower().replace(' ', '')}.com",
            role="Owner",
            shop_id=self.id
        )
        owner.set_password("owner123")  

        worker = User(
            username=f"{self.shop_name.lower().replace(' ', '_')}_worker",
            email=f"worker@{self.shop_name.lower().replace(' ', '')}.com",
            role="Worker",
            shop_id=self.id
        )
        worker.set_password("worker123")  

        db.session.add(owner)
        db.session.add(worker)
        db.session.commit()
    
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    shop = db.relationship('Shop', backref=db.backref('users', lazy=True))
    
    def set_password(self, password):
        from app import bcrypt  
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        from app import bcrypt  
        return bcrypt.check_password_hash(self.password_hash, password)
    
class Document(db.Model):
    __tablename__ = "documents"
    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(3), nullable=False)  # 'in' or 'out'
    total_quantity = db.Column(db.Float, nullable=False, default=0.0)
    received_by = db.Column(db.String(100), nullable=False)
    delivered_by = db.Column(db.String(100), nullable=False)
    supplier = db.Column(db.String(100), nullable=False)
    document_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    # Relationship - when document is deleted, lines are also deleted
    document_lines = db.relationship('DocumentLine', backref='document', lazy=True, cascade='all, delete-orphan')
    
    def update_product_quantities(self):
        """Update product quantities based on document type and lines"""
        for line in self.document_lines:
            product = Product.query.get(line.product_id)
            if product:
                if self.document_type == 'in':
                    # Add quantity for incoming documents
                    product.quantity += line.quantity
                elif self.document_type == 'out':
                    # Subtract quantity for outgoing documents
                    product.quantity -= line.quantity
        db.session.commit()

class DocumentLine(db.Model):
    __tablename__ = "document_lines"
    id = db.Column(db.Integer, primary_key=True)
    parent_document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    # Relationship to Product
    product = db.relationship('Product', backref=db.backref('document_lines', lazy=True))