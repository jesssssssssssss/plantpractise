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
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from shopProducts")
    rows = cur.fetchall()
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

# Here is defining functions that validate address and payment details, ensuring they're entered completely. These functions
#  will be called in the "editAccountDetails" function beneath. 

def validate_address(addressHouseNo, addressStreetName, addressSuburb, addressCity, addressPostCode):
    if addressHouseNo or addressStreetName or addressSuburb or addressCity or addressPostCode:
        if not (addressHouseNo and addressStreetName and addressSuburb and addressCity and addressPostCode):
            return False, "When entering address, please provide complete address information."
    return True, ""     # Empty string is used here to maintain consistent return types within the function. 

def validate_payment(paymentCardNo, paymentCardCvc, paymentCardExp):
    if paymentCardNo or paymentCardCvc or paymentCardExp:
        if not (paymentCardNo and paymentCardCvc and paymentCardExp):
            return False, "When entering payment details, please provide complete Visa Mastercard information."
    return True, ""

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
        
        is_valid_address, addresserrormsg = validate_address(addressHouseNo, addressStreetName, addressSuburb, addressCity, addressPostCode)
        is_valid_payment, paymenterrormsg = validate_payment(paymentCardNo, paymentCardCvc, paymentCardExp)
        
        if not firstName:
            flash("First name is required.", category="error")

        elif not email:
            flash("Email is required.", category="error")

        else:

            if len(firstName) < 2:
                flash("First name must be at least 2 characters.", category="error")
                return redirect(url_for('views.editAccountDetails'))
            
            elif len(lastName) < 2:
                flash("Last name must be at least 2 characters.", category="error")
                return redirect(url_for('views.editAccountDetails'))
            
            elif mobileNo and not re.match(r'^\+?[0-9\s]{9,17}$', mobileNo):
                flash('Invalid input. Mobile number should be 9-17 characters. Only digits, spaces and an optional "+" for area code may be included.', category='error')
                return redirect(url_for('views.editAccountDetails'))
            
            elif not is_valid_address:
                flash(addresserrormsg, category='error')
                return redirect(url_for('views.editAccountDetails')) 
            # ^
            # NOT CURRENTLY WORKING AS INTENDED - STILL WORKING ON VALIDATING COMPLETE ADDRESS/PAYMENT INPUT 
            # v
            elif not is_valid_payment:
                flash(paymenterrormsg, category='error')
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


