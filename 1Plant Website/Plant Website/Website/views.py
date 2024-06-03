from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Product, User, AccountDetails
from flask_sqlalchemy import SQLAlchemy
from . import db 
import json 
import sqlite3 as sql
#NEW ADDITIONS^^

views = Blueprint('views',__name__)

@views.route('/', methods=['GET', 'POST']) 
def home():
    return render_template("home.html", user=current_user) 

@views.route('/shop')
def shop():
    return render_template('shop.html', user=current_user)

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

    if accountDetails.paymentCardNo:
        masked_card = "**** **** **** " + accountDetails.paymentCardNo[-4:]
    else:
        masked_card = None
    

    return render_template('accountDetails.html', user=user, accountDetails=accountDetails, masked_card=masked_card)

@views.route('/editAccountDetails', methods=['GET', 'POST'])
def editAccountDetails():
       
    if request.method == 'POST':
        user_id = current_user.id
        account_details = AccountDetails.query.filter_by(userId=user_id).first()

        account_details.firstName = request.form['firstName']
        account_details.lastName = request.form['lastName']
        account_details.email = request.form['email']
        account_details.mobileNo = request.form['mobileNo']
        account_details.addressHouseNo = request.form['addressHouseNo']
        account_details.addressStreetName = request.form['addressStreetName']
        account_details.addressSuburb = request.form['addressSuburb']
        account_details.addressCity = request.form['addressCity']
        account_details.addressPostCode = request.form['addressPostCode']
        account_details.paymentCardNo = request.form['paymentCardNo']
        account_details.paymentCardCvc = request.form['paymentCardCvc']
        account_details.paymentCardExp = request.form['paymentCardExp']

        db.session.commit()
        flash('Account details updated successfully', category='success')
        return redirect(url_for('views.accountDetails'))
    
    else:
        return render_template("editAccountDetails.html", user=current_user)

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
        

