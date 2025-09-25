from app import db

class Product(db.Model):
    __tablename__ = "products"   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
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
    