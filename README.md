# Tech-Product-Search-Tool

##### This is a tool for web scraping and monitoring prices on tech product stores (such as newegg)
##### Currently, this will ONLY scrape newegg.com, but I intend to implement scrapers for other websites in the future.
##### In addition to being a we scraper, this is also a bot, that will send emails to the user, when a product they're interested in drops below a certain price.
##### The domain currently ruinning this code is www.techproductsearchtool.com

##### Contributions to this code are welcome!  This is my first web app and I'm sure a lot of code could have been implemented better, so please message me with edits or suggestions!
##### Credit to [TechWithTim](https://github.com/techwithtim/Flask-Web-App-Tutorial)https://github.com/techwithtim/Flask-Web-App-Tutorial for the initial design.

## Installation and setup:
###### run this code, first enter the following bash commands:
```bash
git clone <repo-url>
```

```bash
pip install -r requirements.txt
```

## Running the app
##### In order to user the email notification system, you have to replace the text in the 'email_creds.txt' file with your own credentials.
##### The first few minutes of this youtube video explain this better: 
```
https://www.youtube.com/watch?v=zxFXnLEmnb4
```
##### After doing this, the app should run from main, or with the command:
```bash
python main.py
```

## Viewing the app
##### Go to https://127.0.0.1:5000

### This code includes the csv files and results.html page generated from searching '3080' using the web scraping function.
