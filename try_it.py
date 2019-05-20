import time, requests, threading, pandas, datetime, certifi, json, schedule
from bs4 import BeautifulSoup
from datetime import datetime
import http.client, urllib.request, urllib.parse, urllib.error, ssl, base64
from twilio.rest import Client

B = input("give me a B: ")

def YOO():
    try:
        r=requests.get("http://www.pjm.com/markets-and-operations.aspx")
        c=r.content
        soup = BeautifulSoup(c,"html.parser")
        table_body=soup.find('tbody')
        rows = table_body.find_all('tr')

        x=0
        for row in rows:
            x = x + 1
            cols = row.find_all('td')
            cols = [x.text.strip() for x in cols]
            if x == 8:
                DEOK = float(cols[1].strip('$'))
                print(DEOK)

    except:
        DEOK = B
        print(DEOK)

YOO()
