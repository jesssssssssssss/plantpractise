from flask import Flask, render_template, request, flash, Blueprint, current_app
#Importing Contact Form
from .forms import ContactForm
from flask_mail import Message
from flask_login import current_user
#Importing app and mail instances from __init__.py
from . import mail



bp = Blueprint('contact', __name__)

@bp.route('/contact', methods=['GET','POST'])
def contact():
    form = ContactForm()
    success = False #Initalising success as false
 
    if request.method == 'POST':
        #If the inputs are not valid an error will flash and the page will be reloaded
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form, user=current_user)
        #Success message
        else:
            msg = Message(form.subject.data, sender=current_app.config['MAIL_USERNAME'], recipients=['270268490@yoobeestudent.ac.nz','270278266@yoobeestudent.ac.nz', '270045467@yoobeestudent.ac.nz'])
            #Formatting email
            msg.body =f"""
            From: {form.name.data} <{form.email.data}>
            {form.message.data}
            """
            mail.send(msg) #Sending the email
            return render_template('contact.html', success=True, form=form, user=current_user)
    elif request.method == 'GET':
        return render_template('contact.html', form=form, user=current_user)