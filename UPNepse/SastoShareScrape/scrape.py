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


def retrieve_active_company():
    active_comp_symbol = []
    with open('/mnt/d/CollegeProject/UPNepse/data_collection/active_comp.json','r') as comp_data:
        data_json = json.load(comp_data)
        for k,v in data_json.items():
            active_comp_symbol.append(k)

    return active_comp_symbol





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





def write_data_to_file(category_data,company,data):



    create_folder_path = f"/mnt/d/dataStorage/UPNepseDataLake/historicFinancialData/{company}_financial_data"
    create_logs_folder_path = f"/mnt/d/dataStorage/UPNepseDataLake/financialLogs/{company}_financial_logs_data"
    os.makedirs(create_folder_path,exist_ok=True)
    os.makedirs(create_logs_folder_path,exist_ok=True)
    try:
        with open(os.path.join(create_folder_path,f"{category_data}_file.json"),'w') as bf:
            json.dump(data,bf,indent=2)
    except Exception as e:
        with open(os.path.join(create_logs_folder_path,f"{category_data}_error_log_file.txt"),'w') as ef:
            ef.write(f"encountered error while writing to {company} data of data type : {category_data} \n")
            ef.write(f"{e} /n")
            ef.write(f"error time {datetime.now()}")
    else:
        with open(os.path.join(create_logs_folder_path,f"{category_data}_log_file.txt"),'w') as ef:
            ef.write(f"successfully written to {company} data of date : {category_data} \n")
            ef.write(f"success written time {datetime.now()}")



def extract_raw_data(comp_symbol):

    stock_url = f'https://nepsealpha.com/sastoshare/tearsheet/{comp_symbol}'

    driver.get(stock_url)

    sleep(15)

    finacial_btn = driver.find_element(By.XPATH,'//*[@id="custom-financial"]')
    growth_btn = driver.find_element(By.XPATH,'//*[@id="custom-growth"]')
    ratio_btn = driver.find_element(By.XPATH,'//*[@id="custom-key_ratio"]')
    dividend_btn = driver.find_element(By.XPATH,'//*[@id="custom-dividend"]')
    action_btn = driver.find_element(By.XPATH,'//*[@id="custom-corporate-action"]')


    finacial_btn.click()
    sleep(5)
    growth_btn.click()
    sleep(5)
    ratio_btn.click()
    sleep(5)
    dividend_btn.click()
    sleep(5)
    action_btn.click()
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
    list_of_keywords = ['financials','growth','key_ratio','dividend','corporate_action']
    exclude_keywords = ['ajax','what-if-chart']
    records_dictionary = {}
    for log in filter(log_filter, logs):
        request_id = log["params"]["requestId"]
        resp_url = log["params"]["response"]["url"]
        if any(keyword in resp_url for keyword in list_of_keywords):
            if not any(kw in resp_url for kw in exclude_keywords):
                parsed_path= urlparse(resp_url).path
                path_list = (parsed_path.split('/'))
                print(f"Caught {resp_url}")
                file_name =  path_list[-1]
                resp_json_from_net = (driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id}))

                imp_data = {}
                json_resp = json.dumps(resp_json_from_net)
                json_resp_dict = json.loads(json_resp)
                for k,v in json_resp_dict.items():
                   if k == "body":
                       imp_data = json.loads(v)
                       print(imp_data)

                write_data_to_file(file_name,comp_symbol,{file_name:imp_data})


login(username_,password_,"https://nepsealpha.com/login")

active_companies = retrieve_active_company()

for symbol in active_companies:

    check_folder_path = f"/mnt/d/dataStorage/UPNepseDataLake/historicFinancialData/{symbol}_financial_data"
    check_logs_path = f"/mnt/d/dataStorage/UPNepseDataLake/financialLogs/{symbol}_financial_logs_data"
    if os.path.exists(check_folder_path):
        print("data already present for this symbol")
        continue
    extract_raw_data(symbol)
    sleep(2)
    driver.refresh()

print("All fundamental Data captured")
sleep(5)
driver.quit()
