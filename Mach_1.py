import time, requests, threading, pandas, datetime, certifi, json, schedule
from bs4 import BeautifulSoup
from datetime import datetime
import http.client, urllib.request, urllib.parse, urllib.error, ssl, base64
from twilio.rest import Client

SW = 0
df1 = pandas.read_excel("database.xlsx",sheet_name=0)


def text(L):
    account_sid = "AC85b195a1cf7e1f9f3bd44de5944b2ee4"
    auth_token  = "fded6f65560712095459325582bf31b6"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to = "+13059429629", #John - 3059429629 | doug - 5138396035
        from_ = "+17868861537",
        body = "the average price of power is $%.2f more than the day ahead" %L)

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

    #this is the web scraper / ** avg finder **
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

            M = int(datetime.now().strftime('%M'))
            M = M

            df1.iloc[M,0] = DEOK
            M = M + 1
            tot = sum(df1.iloc[0:M,0])
            avg = float((tot/M))
            ts = datetime.now().strftime("%H:%M:%S.%f")


            # make sure it it running right with this check THEEENNNNNN intigrate it
            print("DA: $%.2f" %DA)
            print("RT: $%.2f" %DEOK)
            print("avgerage as of %s -> %.2f" %(ts, avg))
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#************************************ ACTION LINE ************************************
            if avg > (DA + 30) and (10 < min < 30):
                L = avg - DA
                text(L)
                globals()["SW"] = 1

def reset():
    Min = int(datetime.now().strftime('%M'))
    if Min > 50:
        globals()["SW"] = 0

#      ** these line control when the code is actively running **
while True:

    #need some here to make sure the code waits till the begining of the minute to start

    #  DON'T START TILL I TELL YOU TOOOOOOOOOOOOOOO
        #MY NAME IS NOOOOTTTTT  RIIIIIIIICCCCCCCCCKKK




    ts = int(time.strftime('%H'))

    if (7 > ts) or (ts > 17) or (ts == 17):
        print("program is not running")
        time.sleep(60)

    if ((7 < ts) and (ts < 17)) or (ts == 12):
        start_time = time.time()
        if SW == 0:
            rt()
            time.sleep(59)
        else:
            reset()
            time.sleep(60)

        print("total run time -> %s" % (time.time() - start_time))
        print("-----------------------------")
