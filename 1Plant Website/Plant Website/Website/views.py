from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, AccountDetails, ShopProducts, UserCart, OrderItem, Order
from .forms import SearchForm, ContactForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from . import db 
import json 
import sqlite3 as sql
import re

views = Blueprint('views',__name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    products = featuredProducts()
    return render_template("home.html", user=current_user, products=products)
 
@views.route('/featuredProducts')
def featuredProducts():
    #Specifying the products displayed by id
    productIds = [5,3,2,4]
 
    #Creating a session
    session = Session(db.engine)
 
    #Database queries
    products = session.query(ShopProducts).filter(ShopProducts.id.in_(productIds)).all()
 
    session.close()
    return products

#Function that handles seraches and returning product lists. Created to be called when needed in order to be DRY.
def getShopProducts():
    form = SearchForm()
    products = []

    if request.method == 'POST':
        
        if form.validate_on_submit():
            search_term = form.search.data
        if not search_term:
            flash('Please enter a search term', category='error')
        else:
            #Separating the search_term into separate words
            search_term = search_term.strip()
            search_words = search_term.split()

            #Query displaying products that match search_words in their name, summary, description or category
            products = ShopProducts.query.filter(
                (ShopProducts.name.contains(search_term)) |
                (ShopProducts.category.contains(search_term)) |
                (ShopProducts.summary.contains(search_term)) |
                db.or_(*[ShopProducts.description.contains(word) for word in search_words])
            ).all()
            if not products:
                flash('No products found', category='error')
    else:
        products = ShopProducts.query.all()
    return form, products

@views.route('/shop', methods=['GET', 'POST'])
def shopProducts():
    
    form, products = getShopProducts()

    return render_template('shop.html', user=current_user, products=products, form=form)

@views.route('/shopPlants', methods=['GET', 'POST'])
def shopProductsPlants():

    form, products = getShopProducts()

    return render_template('shopPlants.html', user=current_user, products=products, form=form)

@views.route('/shopPlantsCactiSucculents', methods=['GET', 'POST'])
def shopPlantsCactiSucculents():

    form, products = getShopProducts()

    return render_template('shopPlantsCactiSucculents.html', user=current_user, products=products, form=form)

@views.route('/shopPlantsFlowers', methods=['GET', 'POST'])
def shopPlantsFlowers():

    form, products = getShopProducts()
        
    return render_template('shopPlantsFlowers.html', user=current_user, products=products, form=form)

@views.route('/shopPlantsFlowersAnthuriums', methods=['GET', 'POST'])
def shopPlantsFlowersAnthuriums():

    form, products = getShopProducts()
        
    return render_template('shopPlantsFlowersAnthuriums.html', user=current_user, products=products, form=form)

@views.route('/shopPlantsFlowersOrchids', methods=['GET', 'POST'])
def shopPlantsFlowersOrchids():

    form, products = getShopProducts()
        
    return render_template('shopPlantsFlowersOrchids.html', user=current_user, products=products, form=form)

@views.route('/shopPlantsFlowersOther', methods=['GET', 'POST'])
def shopPlantsFlowersOther():

    form, products = getShopProducts()
        
    return render_template('shopPlantsFlowersOther.html', user=current_user, products=products, form=form)

@views.route('/shopPlantsFlowersPeaceLily', methods=['GET', 'POST'])
def shopPlantsFlowersPeaceLily():  

    form, products = getShopProducts()

    return render_template('shopPlantsFlowersPeaceLily.html', user=current_user, products=products, form=form)

@views.route('/shopPlantsFoliage', methods=['GET', 'POST'])
def shopPlantsFoliage():

    form, products = getShopProducts()
        
    return render_template('shopPlantsFoliage.html', user=current_user, products=products, form=form)

@views.route('/shopPlantsFoliageCalathea', methods=['GET', 'POST'])
def shopPlantsFoliageCalathea():

    form, products = getShopProducts()
        
    return render_template('shopPlantsFoliageCalathea.html', user=current_user, products=products, form=form)

@views.route('/shopPlantsFoliageCarnivorous', methods=['GET', 'POST'])
def shopPlantsFoliageCarnivorous():

    form, products = getShopProducts()
        
    return render_template('shopPlantsFoliageCarnivorous.html', user=current_user, products=products, form=form)

@views.route('/shopPlantsFoliageMonstera', methods=['GET', 'POST'])
def shopPlantsFoliageMonstera():

    form, products = getShopProducts()
        
    return render_template('shopPlantsFoliageMonstera.html', user=current_user, products=products, form=form)

@views.route('/shopPlantsFoliageOther', methods=['GET', 'POST'])
def shopPlantsFoliageOther():

    form, products = getShopProducts()
        
    return render_template('shopPlantsFoliageOther.html', user=current_user, products=products, form=form)

@views.route('/shopPlantsFoliagePhilodendron', methods=['GET', 'POST'])
def shopPlantsFoliagePhilodendron():

    form, products = getShopProducts()
        
    return render_template('shopPlantsFoliagePhilodendron.html', user=current_user, products=products, form=form)

@views.route('/shopPlantsFoliageTrailing', methods=['GET', 'POST'])
def shopPlantsFoliageTrailing():

    form, products = getShopProducts()
        
    return render_template('shopPlantsFoliageTrailing.html', user=current_user, products=products, form=form)

@views.route('/shopPotsPlanters', methods=['GET', 'POST'])
def shopProductsPotsPlanters():

    form, products = getShopProducts()
        
    return render_template('shopPotsPlanters.html', user=current_user, products=products, form=form)

@views.route('/shopPotsPlantersPlanters', methods=['GET', 'POST'])
def shopPotsPlantersPlanters():

    form, products = getShopProducts()
        
    return render_template('shopPotsPlantersPlanters.html', user=current_user, products=products, form=form)

@views.route('/shopPotsPlantersPots', methods=['GET', 'POST'])
def shopPotsPlantersPots():

    form, products = getShopProducts()
        
    return render_template('shopPotsPlantersPots.html', user=current_user, products=products, form=form)


@views.route('/shopPlantKits', methods=['GET', 'POST'])
def shopProductsPlantKits():

    form, products = getShopProducts()

    return render_template('shopPlantKits.html', user=current_user, products=products, form=form)

@views.route('/shopGiftCards', methods=['GET', 'POST'])
def shopProductsGiftCards():
    
    form, products = getShopProducts()

    return render_template('shopGiftCards.html', user=current_user, products=products, form=form)

@views.route('/shopSuppliesAccessories', methods=['GET', 'POST'])
def shopProductsSuppliesAccessories():
    
    form, products = getShopProducts()

    return render_template('shopSuppliesAccessories.html', user=current_user, products=products, form=form)

@views.route('/shopSuppliesAccessoriesDecor', methods=['GET', 'POST'])
def shopSuppliesAccessoriesDecor():

    form, products = getShopProducts()
        
    return render_template('shopSuppliesAccessoriesDecor.html', user=current_user, products=products, form=form)

@views.route('/shopSuppliesAccessoriesPlantCare', methods=['GET', 'POST'])
def shopSuppliesAccessoriesPlantCare():

    form, products = getShopProducts()
        
    return render_template('shopSuppliesAccessoriesPlantCare.html', user=current_user, products=products, form=form)

@views.route('/shopSuppliesAccessoriesTools', methods=['GET', 'POST'])
def shopSuppliesAccessoriesTools():

    form, products = getShopProducts()
        
    return render_template('shopSuppliesAccessoriesTools.html', user=current_user, products=products, form=form)

@views.route('/product/<int:id>')
def product(id):

    product = ShopProducts.query.get_or_404(id)

    return render_template('product.html', user=current_user, product=product)

@views.route('/addToCart/<int:productId>', methods=['POST'])
@login_required
def addToCart(productId):
    product = ShopProducts.query.get_or_404(productId)
    existingCartItem = UserCart.query.filter_by(userId=current_user.id, productId=productId).first()

    qty = int(request.form['quantity'])

    if existingCartItem:
        existingCartItem.quantity += qty
        db.session.commit()
        flash('Product quantity updated in cart', category='success')
    else:
        newCartItem = UserCart(userId=current_user.id, productId=productId, quantity=qty)
        db.session.add(newCartItem)
        db.session.commit()
        flash('Product added to cart', category='success')

    return redirect(url_for('views.shopProducts'))

@views.route('/removeFromCart/<int:productId>', methods=['POST'])
@login_required
def removeFromCart(productId):
            
    existingCartItem = UserCart.query.filter_by(userId=current_user.id, productId=productId).first()

    if existingCartItem:
        if existingCartItem.quantity > 1:
            existingCartItem.quantity -= 1
            db.session.commit()
            flash('One of these removed from cart', category='success')
        else:
            db.session.delete(existingCartItem)
            db.session.commit()
            flash('Product removed from cart', category='success')
    else:
            flash('Product not found in cart', category='error')

    return redirect(url_for('views.viewCart'))

 
@views.route('/viewCart', methods=['GET'])
@login_required
def viewCart(): 

    cartItems = UserCart.query.filter_by(userId=current_user.id).all()
    totalPrice = sum(item.shopproduct .price * item.quantity for item in cartItems)
    totalQuantity = sum(item.quantity for item in cartItems)
    return render_template('viewCart.html', user=current_user, cartItems=cartItems, totalPrice=totalPrice, totalQuantity=totalQuantity) 

@views.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html', user=current_user)

@views.route('/accountDetails')
@login_required
def accountDetails():

    userId = current_user.id
    # Fetch user details from the User table
    user = User.query.filter_by(id=userId).first()

    # Fetch account details from the AccountDetails table
    accountDetails = db.session.query(AccountDetails).filter_by(userId=userId).first()

    if accountDetails.paymentCardNo:
        maskedCard = "**** **** **** " + accountDetails.paymentCardNo[-4:]
    else:
        maskedCard = None
    

    return render_template('accountDetails.html', user=user, accountDetails=accountDetails, maskedCard=maskedCard)

# This is defining functions that validate address and payment details, ensuring they're entered completely. These functions
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
        
    user_id = current_user.id
    accountDetails = AccountDetails.query.filter_by(userId=user_id).first()

    if accountDetails.paymentCardNo:
        maskedCard = "**** **** **** " + accountDetails.paymentCardNo[-4:]

    if request.method == 'POST':
        

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
            
            elif lastName and len(lastName) < 2:
                flash("Last name must be at least 2 characters.", category="error")
                return redirect(url_for('views.editAccountDetails'))
            
            elif mobileNo and not re.match(r'^\+?[0-9\s]{9,17}$', mobileNo):
                flash('Invalid input. Mobile number should be 9-17 characters. Only digits, spaces and an optional "+" for area code may be included.', category='error')
                return redirect(url_for('views.editAccountDetails'))
            
            elif not is_valid_address:
                flash(addresserrormsg, category='error')
                return redirect(url_for('views.editAccountDetails')) 
        
            elif not is_valid_payment:
                flash(paymenterrormsg, category='error')
                return redirect(url_for('views.editAccountDetails'))
     
            else:

                accountDetails.firstName = firstName
                accountDetails.lastName = lastName
                accountDetails.email = email
                accountDetails.mobileNo = mobileNo
                accountDetails.addressHouseNo = addressHouseNo
                accountDetails.addressStreetName = addressStreetName
                accountDetails.addressSuburb = addressSuburb
                accountDetails.addressCity = addressCity
                accountDetails.addressPostCode = addressPostCode
                accountDetails.paymentCardNo = paymentCardNo
                accountDetails.paymentCardCvc = paymentCardCvc
                accountDetails.paymentCardExp = paymentCardExp

                db.session.commit()
                flash('Account details updated successfully', category='success')
                return redirect(url_for('views.accountDetails'))
        
    
    else:
        return render_template("editAccountDetails.html", user=current_user, maskedCard=maskedCard) 


@views.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        # Process the order
        userId = current_user.id
        cartItems = UserCart.query.filter_by(userId=userId).all()
        totalAmount = sum(item.quantity * item.shopproduct.price for item in cartItems)

        # Create a new order
        newOrder = Order(userId=userId, totalAmount=totalAmount)
        db.session.add(newOrder)
        db.session.commit()

        # Add items to the order
        for item in cartItems:
            orderItem = OrderItem(
                orderId=newOrder.id,
                productId=item.productId,
                quantity=item.quantity,
                price=item.shopproduct.price
            )
            db.session.add(orderItem)

            # Update stock levels
            item.shopproduct.stock -= item.quantity
            db.session.delete(item)

            # Update account details
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            email = request.form['email']
            addressHouseNo = request.form['addressHouseNo']
            addressStreetName = request.form['addressStreetName']
            addressSuburb = request.form['addressSuburb']
            addressCity = request.form['addressCity']
            addressPostCode = request.form['addressPostCode']
            is_valid_address, addresserrormsg = validate_address(addressHouseNo, addressStreetName, addressSuburb, addressCity, addressPostCode)
            if not firstName:
                flash("First name is required.", category="error")

            elif not email:
                flash("Email is required.", category="error")

            else:

                if len(firstName) < 2:
                    flash("First name must be at least 2 characters.", category="error")
                    return redirect(url_for('views.checkout'))
                
                elif len(lastName) < 2:
                    flash("Last name must be at least 2 characters.", category="error")
                    return redirect(url_for('views.checkout'))
                
                elif not is_valid_address:
                    flash(addresserrormsg, category='error')
                    return redirect(url_for('views.checkout')) 
        
                else:

                    accountDetails.firstName = firstName
                    accountDetails.lastName = lastName
                    accountDetails.email = email
                    accountDetails.addressHouseNo = addressHouseNo
                    accountDetails.addressStreetName = addressStreetName
                    accountDetails.addressSuburb = addressSuburb
                    accountDetails.addressCity = addressCity
                    accountDetails.addressPostCode = addressPostCode

        db.session.commit()
        flash('Delivery details saved', category='success')
        return redirect(url_for('views.payment', orderId=newOrder.id))

    else:
        userId = current_user.id
        cartItems = UserCart.query.filter_by(userId=userId).all()
        totalAmount = sum(item.quantity * item.shopproduct.price for item in cartItems)
        return render_template('checkout.html', cartItems=cartItems, totalAmount=totalAmount, user=current_user)

@views.route('/payment/<int:orderId>', methods=['GET', 'POST'])
@login_required
def payment(orderId):
    
    order = Order.query.get_or_404(orderId)
    userId = current_user.id
    user = User.query.filter_by(id=userId).first()
    orderItems = OrderItem.query.filter_by(orderId=orderId).all()
    totalPrice = sum(item.price * item.quantity for item in orderItems)
    totalQuantity = sum(item.quantity for item in orderItems)

    accountDetails = db.session.query(AccountDetails).filter_by(userId=userId).first()

    if accountDetails.paymentCardNo:
        maskedCard = "**** **** **** " + accountDetails.paymentCardNo[-4:]
    else:
        maskedCard = None

    if request.method == 'POST':

        paymentMethod = request.form.get('paymentMethod')
        if paymentMethod == 'card':
            # Validate and process card payment
            paymentCardNo = request.form.get('paymentCardNo')
            paymentCardExp = request.form.get('paymentCardExp')
            paymentCardCvc = request.form.get('paymentCardCvc')
            paymentCardName = request.form.get('paymentCardName')
            # Perform necessary validation and processing for card payment
            if not paymentCardNo or not paymentCardExp or not paymentCardCvc or not paymentCardName:
                flash('Please fill in all card details.', category='error')
                return redirect(url_for('views.payment', orderId=orderId))
            # Save payment details or process the payment
            
        elif paymentMethod == 'giftcard':
            # Validate and process gift card payment
            giftCardNo = request.form.get('giftCardNo')
            # Perform necessary validation and processing for gift card payment
            if not giftCardNo:
                flash('Please enter the gift card number.', category='error')
                return redirect(url_for('views.payment', orderId=orderId))

       

        flash('Order placed successfully', category='success')
        return redirect(url_for('views.orderConfirmation', orderId=orderId))
 
    return render_template('payment.html', order=order, user=current_user, orderItems=orderItems, totalPrice=totalPrice, totalQuantity=totalQuantity, maskedCard=maskedCard)

@views.route('/orderConfirmation/<int:orderId>', methods=['GET'])
@login_required
def orderConfirmation(orderId):

    order = Order.query.get_or_404(orderId)
    return render_template('orderConfirmation.html', order=order, user=current_user)
