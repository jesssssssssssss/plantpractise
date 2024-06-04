from Website import create_app, mail
from flask import Flask, render_template, request
import sqlite3 as sql
from flask_login import login_user, login_required, logout_user, current_user

app, mail = create_app(mail_instance=mail)

if __name__ == '__main__': 
    app.run(debug=True) 

#!!! To test account details functionality: Login with "bella@email pwpwpwpw"