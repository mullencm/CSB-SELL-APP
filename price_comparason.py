import time, requests, threading, pandas, datetime, certifi, json
from bs4 import BeautifulSoup
from datetime import datetime
import http.client, urllib.request, urllib.parse, urllib.error, ssl, base64
from twilio.rest import Client

SW = 0

def text(L):
    account_sid = "AC85b195a1cf7e1f9f3bd44de5944b2ee4"
    auth_token  = "fded6f65560712095459325582bf31b6"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to = "+13059429629", #John - 3059429629 | doug - 5138396035
        from_ = "+17868861537",
        body = "the current price of power is $%.2f more than the day ahead" %L)

def rt():
    #min is used in the last if statment in this function to make sure the text can only be sent out at the begining of the hour
    min = int(datetime.now().strftime('%M'))

    # this is the API call that gets the DA (Day Ahead price)
    headers = {"Ocp-Apim-Subscription-Key": "bcc0e4a9009c43d79783078e733d1c48"}
    params = urllib.parse.urlencode({"rowCount":"100", "startRow":"1", "fields":"total_lmp_da",
    "datetime_beginning_ept":"CurrentHour", "pnode_id":"124076095"})

    try:
        conn = http.client.HTTPSConnection('api.pjm.com')
        conn.request("GET", "/api/v1/da_hrl_lmps?%s" % params, "{body}", headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        data = response.read()
        conn.close()
        file = open("output.json", "wb")
        file.write(data)
        file.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    data = json.load(open("output.json"))
    DA = data["items"][0]["total_lmp_da"]

    #this is the web scraper that grabs the DEOK (Real Time Price)

    #     **  REPLACE WITH AVERAGE FINDER  **

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # make sure if statment matches above code
            print("DA: $%.2f" %DA)
            print("RT: $%.2f" %DEOK)
            if min < 70:
                print("avg:")
            print("---")
            # **need to change DEOK to the DEOK hourly Average**
            #this is where the condition statments decide to send a text or not

                #consider timer method
                #      **************************************** THE MOST IMPORTANT LINE ***********
            if DEOK > (DA + 30) and min < 30:
                L = DEOK - DA
                text(L)
                globals()["SW"] = 1

def reset():

    # *
    # * **  change reset() to work for the curent situation
    # *

    min = int(datetime.now().strftime('%M'))

    # this is the API call that gets the DA (Day Ahead price)
    headers = {"Ocp-Apim-Subscription-Key": "bcc0e4a9009c43d79783078e733d1c48"}
    params = urllib.parse.urlencode({"rowCount":"100", "startRow":"1", "fields":"total_lmp_da",
    "datetime_beginning_ept":"CurrentHour", "pnode_id":"124076095"})

    try:
        conn = http.client.HTTPSConnection('api.pjm.com')
        conn.request("GET", "/api/v1/da_hrl_lmps?%s" % params, "{body}", headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        data = response.read()
        conn.close()
        file = open("output.json", "wb")
        file.write(data)
        file.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    data = json.load(open("output.json"))
    DA = data["items"][0]["total_lmp_da"]


    #this is the web scraper that grabs the DEOK (Real Time Price)
    r=requests.get("http://www.pjm.com/markets-and-operations.aspx")
    c=r.content
    soup = BeautifulSoup(c,"html.parser")
    table_body=soup.find('tbody')
    rows = table_body.find_all('tr')

    x = 0
    for row in rows:
        x = x + 1
        cols = row.find_all('td')
        cols = [x.text.strip() for x in cols]
        if x == 8:
            DEOK = float(cols[1].strip('$'))
            print("DA : $%.2f" %DA)
            print("RT : $%.2f higher than Day Ahead" %DEOK)
            print("----")
            if DEOK < (1.1 * DA):
                globals()["SW"] = 0


#      ** these line control when the code is actively running **

while True:
    ts = int(time.strftime('%H'))

    if (7 > ts) or (ts > 17) or (ts == 17):
        print("program is not running")
        time.sleep(30)

    if ((7 < ts) and (ts < 17)) or (ts == 12):
        if SW == 0:
            rt()
            time.sleep(30)
        else:
            reset()
            time.sleep(30)






#store those calls in a list/data base - needs MONGO
#call infomation from the DataBase and compare it with DEOK[1]
#write and if statement that will send out a text if needed
