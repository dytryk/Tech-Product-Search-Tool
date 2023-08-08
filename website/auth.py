'''
Author: Dietrich Sinkevitch
Program: Tech Product Search Tool
Date: 08/08/2023
Github Link: https://github.com/dytryk/techproductsearchtool
'''

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Admin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# create the blueprint for authentication
auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    '''
    This function logs in the user or admin.
    It connects to the 'login.html' page and uses the database to determine if the login info matches a user or admin.
    '''
    if request.method == 'POST':
        # get the login data from the html page
        username = request.form.get('username')
        password = request.form.get('password')

        admin = Admin.query.filter_by(username = username).first()
        user = User.query.filter_by(username = username).first()

        if admin:
            # checks and logs in admins and loads the 'admin.html' page
            if admin.password == password:
                flash('Welcome back, sir!', category='success')
                user = admin
                login_user(user, remember = False)
                return redirect(url_for('views.admin'))
            else:
                flash('Incorrect password, please try again.', category = 'error')
        elif user:
            # checks and logs in users and loads the 'products.html' page
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember = False)
                return redirect(url_for('views.products'))
            # handles incorrect entry; if the data entered is not in the database, the login page reloads
            else:
                flash('Incorrect password, please try again.', category = 'error')
        else:
            flash('Username does not exist, would you like to create an account?', category = 'error')

    return render_template("login.html", user = current_user)


@auth.route('/logout')
@login_required
def logout():
    '''
    This function logs out the user and returns them to the home page.
    '''
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    '''
    This function creates an account for a new user.
    It connects to the 'sign_up.html' page and uses the database to save the new user's info.
    An admin account cannot be created this way..
    '''
    if request.method == 'POST':

        # fetches the data from the 'sign_up.html'
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # handles the following errors: 
            # username is already in use, 
            # username is too short, 
            # email is too long, 
            # email does not contain the '@' sign, 
            # passwords don't match, 
            # password is too short 
        user = User.query.filter_by(username=username).first()
        if user:
            flash('username already in use, please try a different username!', category='error')
        elif len(username) < 2:
            flash('Username must be at least 2 character long.', category='error')
        elif (len(email) > 100):
            flash('Please try a shorter email address.', category = 'error')
        elif "@" not in email:
            flash('Email must contain the "@" character.', category = 'error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # saves the new user in the database, and reroutes user to the login page
            new_user = User(username=username, email = email, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=False)
            flash('Account created!', category='success')
            flash('Please login to continue!')
            return redirect(url_for('auth.login'))

    # reloads the page if the information entered is invalid
    return render_template("sign_up.html", user=current_user)