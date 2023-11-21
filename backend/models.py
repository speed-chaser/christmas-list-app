from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from app import db 


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String(512), nullable=False)
    # Define relationships
    lists = db.relationship('List', backref='user', lazy=True)
    interested_in_table = db.Table('interested_in',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
        db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
    )


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password_hash, password)
    
class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    featured = db.Column(db.Boolean, nullable=False, default=True)
    items = db.relationship('Item', backref='List', lazy=True)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(300)) # Will connect to aws s3
    product_link = db.Column(db.String(300))
    price = db.Column(db.Float)
    comments = db.Column(db.String(300))
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)