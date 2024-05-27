from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, AccountDetails, Product
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route('/shop')
def shop():
    return "<p>Shop"

@auth.route('/about-us')
def aboutUs():
    return "<p>About Us"

@auth.route('/contact')
def contact():
    return "<p>Contact"

@auth.route('/login', methods=['GET', 'POST']) # NEW ADDITION BEGIN
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect pw', category='error')
        else: 
            flash ('Email not exist', category='error')


    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signUp', methods=['GET', 'POST'])

def signUp():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')  
        password2 = request.form.get('password2')

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


    return render_template("signUp.html", user=current_user) 


# NEW ADDITION END