from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Product, User, AccountDetails
from flask_sqlalchemy import SQLAlchemy
from . import db 
import json 
import sqlite3 as sql
#NEW ADDITIONS^^

views = Blueprint('views',__name__)

@views.route('/', methods=['GET', 'POST']) # second parameter - NEW ADDITION
def home():
    return render_template("home.html", user=current_user) # second parameter - NEW ADDITION

@views.route('/shop')
def shop():
    return render_template('shop.html', user=current_user)

# NEW ADDITIONS v

@views.route('/viewCart', methods=['GET', 'POST'])
@login_required
def viewCart():
    if request.method == 'POST':
        product = request.form.get('product')

        if len(product) < 1:
            flash('Product is too short', category='eror')
        else: 
            new_product=Product(data=product, user_id=current_user.id)
            db.session.add(new_product)
            db.session.commit()
            flash('Product added', category='success')

    return render_template("viewCart.html", user=current_user)


@views.route('/accountDetails')
@login_required
def accountDetails():

    userId = current_user.id
    # Fetch user details from the User table
    user = User.query.filter_by(id=userId).first()

    # Fetch account details from the AccountDetails table
    accountDetails = db.session.query(AccountDetails).filter_by(userId=userId).first()
    

    return render_template('accountDetails.html', user=user, accountDetails=accountDetails)

@views.route('/editAccountDetails', methods=['POST', 'GET'])
def editAccountDetails():


    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')

        userId = current_user.id
        user = User.query.filter_by(userId=userId).first()

        

    return render_template("editAccountDetails.html", user=current_user, accountDetails=accountDetails) 

@views.route('/completeEdit', methods=['POST', 'GET'])
def completeEdit():
    if request.method == 'GET':
        try:
            UsrID = request.args.get('UsrID')
            firstName = request.args.get('firstName')
            lastName = request.args.get('lastName')
            email = request.args.get('email')
            mobileNo = request.args.get('mobileNo')
            addressHouseNo = request.args.get('addressHouseNo')
            addressStreetName = request.args.get('addressStreetName')
            addressSuburb = request.args.get('addressSuburb')
            addressCity = request.args.get('addressCity')
            addressPostCode = request.args.get('addressPostCode')

            with sql.connect("database.db") as con:
                cur=con.cursor()
                cur.execute("UPDATE AccountDetails SET firstName=?, lastName=?, email=?, mobileNo=?, addressHouseNo=?, addressStreetName=?, addressSuburb=?, addressCity=?, addressPostCode=? WHERE UsrID=?", (firstName, lastName, email, mobileNo, addressHouseNo, addressStreetName, addressSuburb, addressCity, addressPostCode, UsrID))
                msg = "Data updated success"
                con.commit()
        
        except: 
            msg = "error in update"
            con.rollback()
            
        finally:
            return render_template("completeEdit.html", msg=msg)
            

''' 
First attempt:

    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur=con.cursor()
    cur.execute("select * from AccountDetails where userId=?")
    rows=cur.fetchall()
    return render_template("editAccountDetails.html", rows=rows)

signup format:

@views.route('/editAccountDetails')
def editAccountDetails():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        mobileNo = request.form.get('mobileNo')  
        addressHouseNo = request.form.get('addressHouseNo')
        addressStreetName = request.form.get('addressStreetName')
        addressSuburb = request.form.get('addressSuburb')
        addressCity = request.form.get('addressCity')
        addressPostCode = request.form.get('addressPostCode')

        userId = current_user.id
        user = User.query.filter_by(email=email).first()

        if user: 
            flash('email already exist', category='error')

        elif len(email) < 4:
            flash('Email must be more than 3 characters.', category='error')
            
        elif len(firstName) < 2:
            flash('First name must be more than 1 character.', category='error')
            
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
            
        elif len(password1) < 7:
            flash('Password too short', category='error')
            
        else:
            new_user=User(email=email, firstName=firstName, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            
            userId = new_user.id
            newAccDetails = AccountDetails(userId=userId, firstName=firstName, email=email)
            db.session.add(newAccDetails)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home', new_user=current_user))


    return render_template("editAccountDetails.html", user=current_user) '''



''' @views.route('/login') # NEW ADDITION 
def login():
    return render_template('login.html')''' 


''' @views.route('/accountDetails')
@login_required
def accountDetails():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur=con.cursor()
    cur.execute("Select * from AccountDetails")
    rows=cur.fetchall()
    return render_template('accountDetails.html', rows=rows, user=current_user) '''

