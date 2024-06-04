from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Product, User, AccountDetails
from flask_sqlalchemy import SQLAlchemy
from . import db 
import json 
import sqlite3 as sql
import re

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

        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        mobileNo = request.form['mobileNo']
        addressHouseNo = request.form['addressHouseNo']
        addressStreetName = request.form['addressStreetName']
        addressSuburb = request.form['addressSuburb']
        addressCity = request.form['addressCity']
        addressPostCode = request.form['addressPostCode']
        paymentCardNo = request.form['paymentCardNo']
        paymentCardCvc = request.form['paymentCardCvc']
        paymentCardExp = request.form['paymentCardExp']

        # Validation happens here. Please Note: firstName attribute is being tested with both client-side validation 
        #  (by using the "required" keyword in the html file), and with server-side validation, here. This is because
        #  using just client-side validation in any context isn't completely secure and can be bypassed by users that
        #  have developer tools and knowledge, and adding server-side validation provides extra security. Therefore,
        #  the use of both these methods is not in conflict with the DRY principle. 
        
        if not firstName:
            flash("First name is required", category="error")

        elif not email:
            flash("Email is required", category="error")

        else:
            if len(mobileNo) < 5:
                flash("Mobile num must be at least 5 digits", category="error")
                return redirect(url_for('views.editAccountDetails'))

            elif len(firstName) < 2:
                flash("first nam must be at least 2 characters", category="error")
                return redirect(url_for('views.editAccountDetails'))
            
     
            else:

                account_details.firstName = firstName
                account_details.lastName = lastName
                account_details.email = email
                account_details.mobileNo = mobileNo
                account_details.addressHouseNo = addressHouseNo
                account_details.addressStreetName = addressStreetName
                account_details.addressSuburb = addressSuburb
                account_details.addressCity = addressCity
                account_details.addressPostCode = addressPostCode
                account_details.paymentCardNo = paymentCardNo
                account_details.paymentCardCvc = paymentCardCvc
                account_details.paymentCardExp = paymentCardExp

                db.session.commit()
                flash('Account details updated successfully', category='success')
                return redirect(url_for('views.accountDetails'))
        
    
    else:
        return render_template("editAccountDetails.html", user=current_user) 


