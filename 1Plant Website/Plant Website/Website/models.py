from . import db
from flask_login import UserMixin
from sqlalchemy import func 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    products = db.relationship('ShopProducts', backref='user')
    cart = db.relationship('UserCart', lazy=True)

 
class AccountDetails(db.Model):
    __tablename__ = 'AccountDetails'
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(150), nullable=True)
    mobileNo = db.Column(db.String(15), nullable=True)
    addressHouseNo = db.Column(db.String, nullable=True)
    addressStreetName = db.Column(db.String, nullable=True)
    addressSuburb = db.Column(db.String, nullable=True)
    addressCity = db.Column(db.String, nullable=True)
    addressPostCode = db.Column(db.String, nullable=True)
    paymentCardNo = db.Column(db.String(4), nullable=True)
    paymentCardCvc = db.Column(db.Integer, nullable=True)
    paymentCardExp = db.Column(db.String, nullable=True)
    user = db.relationship('User', backref=db.backref('AccountDetails', uselist=False))
 
class ShopProducts(db.Model):
    __tablename__ = 'shopProducts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False) #Is required
    summary = db.Column(db.String(500), nullable=True)
    description = db.Column(db.String(1000), nullable=True)
    price = db.Column(db.Integer, nullable=False) #Is required
    stock = db.Column(db.Integer, nullable=False) #Is required
    category = db.Column(db.String(150), nullable=False) #Is required
    subCategory = db.Column(db.String(150), nullable=True)
    subSubCategory = db.Column(db.String(150), nullable=True)
    imageUrl = db.Column(db.String(150), nullable=False) #Is required
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
 
class UserCart(db.Model):
    __tablename__ = 'UserCart'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    productId = db.Column(db.Integer, db.ForeignKey('shopProducts.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    shopproduct = db.relationship('ShopProducts')
    user = db.relationship('User')
    

 
# shopproduct = db.relationship('ShopProducts', backref=db.backref('userCart', uselist=False (? maybe make uselist=true) ))




    