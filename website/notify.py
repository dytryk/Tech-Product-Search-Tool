'''
Author: Dietrich Sinkevitch
Program: Tech Product Search Tool
Date: 08/08/2023
Github Link: https://github.com/dytryk/techproductsearchtool
'''

import smtplib
from flask import Flask
import ssl
from email.message import EmailMessage
from bs4 import BeautifulSoup
import requests
import sys
from pathlib import Path
sys.path.insert(0, str(Path("models.py").resolve().parent))
from website.models import User, db


# create seperate instance of the app
DB_NAME = "database.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)


def search_link(link, amount, name):
    '''
    This function searches for a particular link and returns its list containing the items name, price, and link.
    It is called by the email_user function.
    '''
    info = []
    url = link
    price_check = float(amount)  # Convert the amount to float

    # checks if this link is from newegg.  I intend to add scrapers for more websites but newegg was a good placr to start.
    if "https://www.newegg.com" in url:
        response = requests.get(url)
        # checks if the response code is good and pulls the html data
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            product_container = soup.select('div.page-section-inner')
            for container in product_container:
                #try getting the price data from the html
                try:
                    price_element = container.select_one('li.price-current strong')
                    if price_element:
                        price = price_element.get_text(strip=True)
                        price = float(price.replace('$', '').replace(',', ''))  # Convert to float
                        # if the product price has dropped below the price set by the user, this product is added to the list
                        if price < price_check:
                            info.append(name)
                            info.append(price)
                            info.append(link)
                except Exception as e:
                    print(f"Error processing container: {e}")

            return info
        else:
            print(f'Error: Unable to fetch data from {url}. Status code: {response.status_code}')


def email_user(username, email, user_id):
    '''
    This function emails a user a list of their products which have dropped below the set price.
    It calls the 'search_link' function and is called by the 'notify_all_users' function.
    '''
    with app.app_context():
        # Define email sender and receiver
        email_sender = ''
        email_password = ''
        # The email credentials are saved in a .txt file, so this reads them in
        with open('email_creds.txt') as creds:
            cred_list = creds.readlines()
            email_password = cred_list[0]
            email_sender = cred_list[1]
        email_receiver = email
        price_changes = []

        # load in the user from the database
        user = User.query.get(user_id)

        if user:
            products = user.products
            # try except to dealm with users who don't have any saved products
            try:
                for product in products:
                    #loop through all the products that the current user has saved 
                    # and proceed to checking the link if the user has selected this product to be monitored (product.search == 1)
                    if (product.user_id == user_id) and (product.search == 1):
                        # call the 'search_link' function on the product to see if it's price is below the set price
                        product_info = search_link(product.link, product.price, product.name)
                        try:
                            if product_info != []:
                                # if 'search_link' returns a valid list, append the values to the local list
                                index = 0
                                for info in product_info:
                                    price_changes.append(product_info[index])
                                    index += 1
                        except:
                            pass
            except:
                pass
        
        # save a string of all the products to notify the user about by iterating through the list of product info
        price_changes_formatted = ""
        i = 0
        while i < len(price_changes):
            price_changes_formatted = price_changes_formatted + f"{price_changes[i]}\n${price_changes[i + 1]}\n{price_changes[i + 2]}\n\n"
            i = i + 3

        # Set the subject and body of the email
        subject = "Product Price Drop!"
        body = f"""Hi, {username}!\n\nThe following products have dropped in price to below your set amount:\n\n{price_changes_formatted}Happy shopping!\n
        -Tech Product Deals\n\nP.S. depending on your location, prices may differ from our reported prices."""

        # format the email message
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())


def notify_all_users():
    '''
    This function goes through the database and calls the 'email_user' function for all the users
    '''
    with app.app_context():
        # loop through the user table from the database
        try:
            index = 1
            while True:
                user = User.query.get(index)
                email_user(user.username, user.email, user.id)
                index += 1
        except:
            pass