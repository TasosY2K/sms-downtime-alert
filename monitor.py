import time
import requests
import schedule
import validators
import json
import sys
import os.path
from twilio.rest import Client

config_path = "./config.json"

if os.path.isfile(config_path):
    print("[CONFIG] Config file " + config_path + " found")
    f = open("./config.json", "r")
    cfg = json.loads(f.read())
    account_sid = cfg["account_sid"]
    auth_token = cfg["auth_token"]
    url = cfg["url"]
    if validators.url(url) == False:
        print("[ERROR] The provided URL: " + url + " is not valid")
        sys.exit()
    recieve_number = cfg["recieve_number"]
    send_number = cfg["send_number"]
    interval = int(cfg["interval"])
    if interval < 1 or interval > 60:
        print("[ERROR] The provided interval: " + str(interval) + " is not in range (1-60)")
        sys.exit()
    f.close()
else:
    print("[CONFIG] Config file " + config_path + " not found")
    sys.exit()

def send_sms():
    client = Client(account_sid, auth_token)
    message = client.messages.create(to=recieve_number, from_=send_number, body="Your site: " + url + " seems to be down :(")

def send_request():
    try:
        requests.get(url)
    except requests.exceptions.ConnectionError:
        send_sms()
        print("[DOWN] " + url + " is down")
        print("[SMS] Sending SMS alert to " + recieve_number)
    else:
        print("[UP] " + url + " seems to be up")

schedule.every(interval).minutes.do(send_request)

while True:
    schedule.run_pending()
    time.sleep(1)
