import time
import datetime
import schedule
from datetime import datetime


def job():
    ts = datetime.now().strftime("%H:%M:%S.%f")
    print("I am doing this job!")
    print("curren time is %s" %ts)

schedule.every().monday.at("8:58").do(job)
schedule.every().monday.at("9:00").do(job)
schedule.every().monday.at("9:01").do(job)
schedule.every().monday.at("9:02").do(job)
schedule.every().monday.at("9:03").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
