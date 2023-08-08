'''
Author: Dietrich Sinkevitch
Program: Tech Product Search Tool
Date: 08/08/2023
Github Link: https://github.com/dytryk/techproductsearchtool
'''

from bs4 import BeautifulSoup
import requests
import warnings
import csv
import pandas as pd

# this prevents a certain annoying warning that was messing with the code excecution
warnings.filterwarnings("ignore", category = DeprecationWarning)


def sort_by_price(product):
    '''
    This function is a helper function for sorting by price.
    '''
    return float(product[' price:'])


def read_csv(file_name):
    '''
    This function reads in a csv and returns the contents as a list.
    '''
    with open(file_name, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def write_to_csv(data):
    '''
    This function turns a list of product information into a csv file, and returns the lowest, highest, and avergae price of all the products.
    '''
    # declare variable for calculations at the end
    min_price = 100000
    max_price = 0
    total_cost = 0
    num_products = 1 # set to one to avoid division by zero errors
    avgp = 0

    # create or select the csv file
    with open('deals.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['product name:', ' price:', ' link:']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        # write the data line by line from the list
        for product in data:
            try:
                if (product[' price:'] != '0'):
                    writer.writerow(product)
                    price = int(product[' price:'])
                    # find the max and min prices
                    if (price > max_price):
                        max_price = price
                    if (price < min_price):
                        min_price = price
                    num_products = num_products + 1
                    total_cost = total_cost + price
            except:
                pass
    
    # caululate the average price and return a string containing the lowest, highest, and average price
    avgp = total_cost/num_products
    avg_price = int(avgp)
    prices = f"Lowest price: ${min_price}, Average price: ${avg_price}, Highest price: ${max_price}"
    return prices


def write_to_sorted_csv(data):
    '''
    This function writes a csv file of all the products sorted by price.
    '''
    with open('sorted_deals.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['product name:', ' price:', ' link:']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def csv_to_html():
    '''
    This function writes a html webpage that has all the functionality of the home page, but with a table of all the data below the search bar.
    '''
    df = pd.read_csv('sorted_deals.csv')
    html_table = df.to_html(justify = 'left', index=False, show_dimensions=True, render_links=True, col_space=100, )

    # the next few lines create a new html page called 'results.html'.
    # the beginning of this file will be the 'home_start.html' file, 
    # then an html table containing all the product data will be add, 
    # finally, the file will end with the price data and ending html tags.
    with open('website/templates/home_start.html', 'r', encoding='utf-8') as source:
        with open('website/templates/results.html', 'w', encoding='utf-8') as target:
            for line in source:
                target.write(line)
            target.write(html_table)
            target.write("</div></body><br><h5 align = center>{{dataToRender}}</h5></form>{% endblock %}")


def newegg(product):
    '''
    This function searches newegg.com for products and pulls the price, name, price, and link of each product that newegg returns.
    It is called by the 'deals' function.
    It takes a string of the term you want to search for.
    '''

    newegg_deals = []

    # format the rquest and get the html from the page
    url = f"https://www.newegg.com/p/pl?d={product}&PageSize=96"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    # find out how many pages of results there are (this is set to 96 items per page)
    num_pages = 1
    try:
        pagination = doc.find(class_ = "list-tool-pagination-text").strong
        num_pages = int(str(pagination).split("/")[-2].split(">")[-1][:-1])
    except:
        pass

    print("the number of pages this search returned is: " + num_pages)

    # loop through the pages and get the html for each page
    for page in range(1, num_pages + 1):
        url = f'https://www.newegg.com/p/pl?d={product}&PageSize=96&page={page}'
        response = requests.get(url, headers=headers)

        # if all is well, find the item containers in the page
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            product_containers = soup.select('div.item-container')

            # loop through the containers and pull out the product name, price, and link
            for container in product_containers:
                product = {}
                try:
                    product['product name:'] = container.select_one('a.item-title').text.strip()
                    product[' price:'] = container.select_one('li.price-current strong').text.strip().replace(',', '')
                    product[' link:'] = container.select_one('a.item-title')['href']
                except:
                    pass
                # append the product data to the newegg list
                newegg_deals.append(product)
        else:
            print(f'Error: Unable to fetch data from {url}. Status code: {response.status_code}')
    return newegg_deals


'''
the following functions have not been set up yet, but the sites might be useful for getting more data later.  
The code is designed to ruin using all of the functions, so long as they allreturn the same data type.
'''

def adorama(product):
    '''
    This function searches adorama.com for products and pulls the price, name, price, and link of each product that newegg returns.
    It is called by the 'deals' function
    This function has not been set up yet, so far only the scraper for newegg has been written.
    '''
    adorama_deals = [" "]


    # url = f"https://www.adorama.com/l/?searchinfo={product}&sf=Relevance&st=de"
    # page = requests.get(url).text
    # doc = BeautifulSoup(page, "html.parser")

    # print(doc)

    return adorama_deals


def bandh(product):
    '''
    This function searches bandh.com for products and pulls the price, name, price, and link of each product that newegg returns.
    It is called by the 'deals' function
    This function has not been set up yet, so far only the scraper for newegg has been written.
    '''
    bandh_deals = []

    # url = f"https://www.bhphotovideo.com/c/search?q={product}&sts=ma"
    # page = requests.get(url).text
    # doc = BeautifulSoup(page, "html.parser")

    # print(doc)

    return bandh_deals


def amazon(product):
    '''
    This function searches amazon.com for products and pulls the price, name, price, and link of each product that newegg returns.
    It is called by the 'deals' function
    This function has not been set up yet, so far only the scraper for newegg has been written.
    '''
    amazon_deals = []

    # url = f"https://www.amazon.com/s?k={product}&i=electronics&crid=3JIHXT2TP2NA0&sprefix=%2Celectronics%2C86&ref=nb_sb_ss_recent_1_0_recent"
    # page = requests.get(url).text
    # doc = BeautifulSoup(page, "html.parser")

    # print(doc)

    return amazon_deals


def bestbuy(product):
    '''
    This function searches bestbuy.com for products and pulls the price, name, price, and link of each product that newegg returns.
    It is called by the 'deals' function
    This function has not been set up yet, so far only the scraper for newegg has been written.
    '''
    bestbuy_deals = []

    # url = f"https://www.bestbuy.com/site/searchpage.jsp?st={product}&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys"
    # page = requests.get(url).text
    # doc = BeautifulSoup(page, "html.parser")

    # print(doc)

    return bestbuy_deals


def microcenter(product):
    '''
    This function searches microcenter.com for products and pulls the price, name, price, and link of each product that newegg returns.
    It is called by the 'deals' function
    This function has not been set up yet, so far only the scraper for newegg has been written.
    '''
    microcenter_deals = []

    # url = f"https://www.microcenter.com/search/search_results.aspx?N=&cat=&Ntt={product}&searchButton=search"
    # page = requests.get(url).text
    # doc = BeautifulSoup(page, "html.parser")

    # print(doc)

    return microcenter_deals


def techbargains(product):
    '''
    This function searches techbargains.com for products and pulls the price, name, price, and link of each product that newegg returns.
    It is called by the 'deals' function
    This function has not been set up yet, so far only the scraper for newegg has been written.
    '''
    techbargain_deals = []

    # url = f"https://www.techbargains.com/search?search={product}"
    # page = requests.get(url).text
    # doc = BeautifulSoup(page, "html.parser")

    # print(doc)

    return techbargain_deals


def walmart(product):
    '''
    This function searches walmart.com for products and pulls the price, name, price, and link of each product that newegg returns.
    It is called by the 'deals' function
    This function has not been set up yet, so far only the scraper for newegg has been written.
    '''
    walmart_deals = []

    # url = f"https://www.walmart.com/search?q={product}"
    # page = requests.get(url).text
    # doc = BeautifulSoup(page, "html.parser")

    # print(doc)

    return walmart_deals


def bensbargains(product):
    '''
    This function searches bensbargains.com for products and pulls the price, name, price, and link of each product that newegg returns.
    It is called by the 'deals' function
    This function has not been set up yet, so far only the scraper for newegg has been written.
    '''
    bensbargains_deals = []


    # url = f"https://bensbargains.com/search/{product}/?savesearch=1"
    # page = requests.get(url).text
    # doc = BeautifulSoup(page, "html.parser")

    # print(doc)

    return bensbargains_deals


deals_all = []

def deals(product):
    '''
    This function is the master function for the whole web scraper.  
    While it will only display results from newegg right now, it is set upn to display results from any number of websites so long as they all return a list datatype.
    '''

    neg = newegg(product)
    adr = adorama(product)
    bah = bandh(product)
    amz = amazon(product)
    bby = bestbuy(product)
    mcr = microcenter(product)
    tbs = techbargains(product)
    fry = walmart(product)
    bbs = bensbargains(product)

    sites = [neg, adr, bah, amz, bby, mcr, tbs, fry, bbs]
    deals_all = []

    # concatonate all the results together
    for site in sites:
        deals_all.extend(site)

    # write the data to a csv and find the min, max, and anv price
    minmax = write_to_csv(deals_all)

    # sort the csv and write it ti a new file
    products = read_csv("deals.csv")
    sorted_deals = sorted(products, key=sort_by_price)
    write_to_sorted_csv(sorted_deals)
    
    # create the html page to display the results
    csv_to_html()

    return minmax