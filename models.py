from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Product_details(db.Model):
    __tablename__ = 'product_details'
    
    id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(100), nullable=False)
    p_price = db.Column(db.Float, nullable=False)
    p_category = db.Column(db.String(50), nullable=False)
    p_stock = db.Column(db.Integer, nullable=False)
    p_description = db.Column(db.String(200), nullable=True)
    p_img = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'{self.id}:{self.p_name}'
    
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    password = db.Column(db.String(200), nullable = False)
    role = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return f'{self.id}:{self.username}'


