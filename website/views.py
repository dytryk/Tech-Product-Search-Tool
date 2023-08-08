'''
Author: Dietrich Sinkevitch
Program: Tech Product Search Tool
Date: 08/08/2023
Github Link: https://github.com/dytryk/techproductsearchtool
'''

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import fresh_login_required, current_user, logout_user
from .models import Admin, Product
from . import db
from .search import *
import json
from sqlalchemy import text

# create the blueprint
views = Blueprint('views', __name__)


@views.route('/', methods = ['GET', 'POST'])
def home():
    '''
    This function defines the home page.
    '''
    if request.method == 'POST':
        # get the search query from the user entry
        product = request.form.get('product')
        # the runs the deals function, 'results' is only the string containing the min, max, and average price
        results = deals(product)
        # renders the 'results.html' page, since the 'home.html' page is not longer neccessary
        return render_template("results.html", user = current_user, dataToRender = results)
    return render_template("home.html", user = current_user)


@views.route('/products', methods=['GET', 'POST'])
@fresh_login_required
def products():
    '''
    This function defines the products page, which is displayed by the 'products.html' page.
    '''
    if request.method == 'POST': 
        # fetch the data from the user input
        name = request.form.get('name')
        link = request.form.get('link')
        price = request.form.get('price')
        price_as_int = None
        try: 
            price_as_int = int(price)
        except: 
            pass
        # check to make sure all the input for saving a new product is valid
        if len(name) > 99:
            flash('The product name is too long, please try something shorter.', category = 'error')
        elif len(name) < 1:
            flash('please enter a name for your product.', category = 'error')
        elif (len(link) < 10) or ("https://" not in link):
            flash('Please enter a valid link!', category='error') 
        elif len(link) > 999:
            flash('please enter a shorter link.', category = 'error')
        elif not isinstance(price_as_int, int):
            flash('please enter a positive integer for the price. (i.e. "100", not "99.99")', category = 'error')
        else:
            # save the new product ion the database
            new_product = Product(name = name, link = link, price = price, user_id = current_user.id, search = 0)  #providing the schema for the note 
            db.session.add(new_product) #adding the note to the database 
            db.session.commit()
            flash('Your new product has been saved!', category='success')

    return render_template("products.html", user=current_user)


@views.route('/delete-product', methods=['POST'])
def delete_product():  
    '''
    This function deletes a product from the database.
    '''
    # this expects a JSON from the INDEX.js file, which will return the product id
    product = json.loads(request.data)
    productID = product['id']
    # query the database to check if the product exists
    product = Product.query.get(productID)
    if product:
        if product.user_id == current_user.id:
            # delete the product from the database
            db.session.delete(product)
            db.session.commit()

    return jsonify({})


@views.route('/select-product', methods=['POST'])
def select_product():  
    '''
    This function swaps whether or not a product is marked for automatic searching (this is for the notification system).
    '''
    # this expects a JSON from the INDEX.js file, which will return the product id
    product = json.loads(request.data) 
    productID = product['id']
    # query the database to check if the product exists
    product = Product.query.get(productID)
    if product:
        if product.user_id == current_user.id:
            # swap the value of 'product.search' between 0 and 1
            value = 0
            if product.search == 0:
                value = 1
            # excecute the SQL to change the value in the database
            sql_query = text("UPDATE product SET search = :new_value WHERE id = :condition_value")
            params = {"new_value": value, "condition_value": product.id}
            db.session.execute(sql_query, params)
            db.session.commit()

    return jsonify({})


@views.route('/admin', methods=['GET', 'POST'])
@fresh_login_required
def admin():
    '''
    This function defines the admin page.
    '''
    id = current_user.id
    formatted_id = f"<Admin {current_user.id}>"
    admin_id = Admin.query.filter_by(id = id).first()
    # makes sure the user trying to access this page is an admin
    if str(formatted_id) == str(admin_id):
        return render_template("admin.html", user = current_user)
    else:
        logout_user()
        return redirect(url_for('auth.login'))