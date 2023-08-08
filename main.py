'''
Author: Dietrich Sinkevitch
Program: Tech Product Search Tool
Date: 08/08/2023
Github Link: https://github.com/dytryk/techproductsearchtool
'''

from website import create_app
import time
import schedule
import threading
import sys
from pathlib import Path
sys.path.insert(0, str(Path("website/notify.py").resolve().parent))
from website.notify import notify_all_users

app = create_app()

def job():
    '''
    The function calls 'notify_all_users' function from 'notify.py'
    '''
    notify_all_users()
    print("emailed users")

# Clear any previously scheduled jobs
schedule.clear()

# Schedule the job to run at 4 AM every day
schedule.every().day.at("04:00").do(job)

schedule_lock = threading.Lock()

def run_schedule():
    '''
    This function runs the schedule to notify users.
    '''
    while True:
        with schedule_lock:
            schedule.run_pending()
            # Check every minute
            time.sleep(60)  

# run the flask app
if __name__ == '__main__':
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()
    app.run(debug=True)