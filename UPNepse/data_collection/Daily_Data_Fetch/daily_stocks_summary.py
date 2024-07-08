from time import sleep
import requests
from dotenv import load_dotenv
import re
import os
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import json
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service



options = webdriver.ChromeOptions()

options.set_capability("goog:loggingPrefs",{"performance":"ALL"})
#options.add_argument("--headless")
service = Service(executable_path="/usr/local/bin/chromedriver")
driver = uc.Chrome(options=options,service=service)
load_dotenv()
username_ = os.getenv('USERNAME')
password_ = os.getenv('PASSWORD')







def login(username,password,url):
    driver.get(url)
    form_el  = driver.find_element(By.XPATH,'/html/body/main/div/div/div/div/div/form')
    username_field_el = form_el.find_element(By.XPATH,'//*[@id="username"]')

    password_field_el = form_el.find_element(By.XPATH,'//*[@id="password"]')

    login_btn = form_el.find_element(By.XPATH,'/html/body/main/div/div/div/div/div/form/button')


    username_field_el.send_keys(username)
    password_field_el.send_keys(password)
    login_btn.click()

    print("----------------------------------------YES-----------------------------")
    print("\nLOGIN SUCESSFULL\n")
    print("----------------------------------------YES-----------------------------")
    sleep(5)





def write_data_to_file(date,data):
    
    data_folder_path = f"/mnt/d/dataStorage/UPNepseDataLake/dailyStocksFetch/marketData"
    logs_folder_path = f"/mnt/d/dataStorage/UPNepseDataLake/dailyStocksFetch/marketLogs"
    if os.path.exists((os.path.join(data_folder_path,f"{date}_summary.json"))):
        return 0

    try:
        with open(os.path.join(data_folder_path,f"{date}_summary.json"),'w') as bf:
            json.dump(data,bf,indent=2)
    except Exception as e:
        with open(os.path.join(logs_folder_path,f"{date}_error_summary.txt"),'w') as ef:
            ef.write(f"encountered error while writing to {date} data of data type   \n")
            ef.write(f"{e} /n")
            ef.write(f"error time {datetime.now()}")
    else:
        with open(os.path.join(logs_folder_path,f"{date}_success_summary.txt"),'w') as ef:
            ef.write(f"success fully written of {date} data of  market summary \n")
            ef.write(f"write time {datetime.now()}")
    return 1


def extract_raw_data():

    logs_folder_path = f"/mnt/d/dataStorage/UPNepseDataLake/dailyStocksFetch/marketLogs"
    stock_url = 'https://nepsealpha.com/sastoshare/live-trading/stocks'

    driver.get(stock_url)

    sleep(5)



    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

    def log_filter(log_):
        return (
            # is an actual response
            log_["method"] == "Network.responseReceived"
            # and json
            and "json" in log_["params"]["response"]["mimeType"]
        )
    records_dictionary = {}
    for log in filter(log_filter, logs):
        request_id = log["params"]["requestId"]
        resp_url = log["params"]["response"]["url"]
        parsed_path= urlparse(resp_url).path
        path_list = (parsed_path.split('/'))
        print(f"Caught {resp_url}")
        if 'stocks-live' in resp_url:
            resp_json_from_net = (driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id}))

            imp_data = {}
            json_resp = json.dumps(resp_json_from_net)
            json_resp_dict = json.loads(json_resp)
            for k,v in json_resp_dict.items():
               if k == "body":
                   imp_data = json.loads(v)
                   print(imp_data.keys())
                   un_date = imp_data['asOf']
                   date_ar = un_date.split(' ') 
                   date = date_ar[0]
                   feedback = write_data_to_file(date,imp_data)
                   with open(os.path.join(logs_folder_path,'logs.txt'),'+a') as sumF:
                        if feedback == 1:
                            sumF.write(f"market data of {date} written at {datetime.now() } success \n")
                        elif feedback == 0:
                            sumF.write(f" ---- ERRROR --- market data of {date} written at {datetime.now() } already present \n")
                            


                    



login(username_,password_,"https://nepsealpha.com/login")
extract_raw_data()

sleep(5)
driver.quit()
