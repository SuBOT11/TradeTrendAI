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
import pandas as pd


options = webdriver.ChromeOptions()
options.set_capability("goog:loggingPrefs",{"performance":"ALL"})
#options.add_argument('--headless')
service = Service(executable_path="/usr/local/bin/chromedriver")
driver = uc.Chrome(options=options,service=service)
wait = WebDriverWait(driver, 5)





def retrieve_comp():
    url = "https://eng.merolagani.com/handlers/AutoSuggestHandler.ashx?type=Company"
    res = requests.get(url).json()
    company_list = []
    for r in res:
        company_list.append(r['d'])

    return company_list

def retrieve_individual_histori_data(comp_symbol):

    data_to_be_framed = {}
    new_stockdate_list= []
    url = 'https://nepsealpha.com/trading/chart?symbol=UPPER'
    ret_url = f"https://nepsealpha.com/trading/chart?symbol={comp_symbol}"
    driver.get(ret_url)
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
    #list_of_keywords = ['financials','growth','key_ratio','dividend','corporate_action']
    keyword = 'history'
    print(keyword)
    #exclude_keywords = ['ajax','what-if-chart']
    records_dictionary = {}
    for log in filter(log_filter, logs):
        request_id = log["params"]["requestId"]
        resp_url = log["params"]["response"]["url"]
        if 'history' in resp_url:
            print('caught' + resp_url)

            resp_json_from_net = (driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id}))
            print(resp_json_from_net)


            imp_data = {}
            json_resp = json.dumps(resp_json_from_net)
            json_resp_dict = json.loads(json_resp)
            for k,v in json_resp_dict.items():
               if k == "body":
                   imp_data = json.loads(v)
                   print(imp_data)


            for key,value in imp_data.items():
                if key == 't':
                     for ts in value:
                         new_time_obj = datetime.fromtimestamp(ts)
                         formatted_datetime_obj = new_time_obj.strftime("%Y-%m-%d")
                         new_stockdate_list.append(formatted_datetime_obj)
                     data_to_be_framed["Date"]  = new_stockdate_list

                if key == 'o':
                    data_to_be_framed["Open"] = value

                if key == 'h':
                    data_to_be_framed["High"] = value

                if key == 'l':
                    data_to_be_framed["Low"] = value

                if key == 'c':
                    data_to_be_framed["Close"] = value

                if key == 'v':
                    data_to_be_framed["Volume"] = value

    return data_to_be_framed

def saving_files_to_datalake():
    logs_directory= f"/mnt/d/dataStorage/UPNepseDataLake/historicNepseData/sslogs"
    list_comp = retrieve_comp()

    for company in list_comp:
        try:
            company_data_dictionay = retrieve_individual_histori_data(company)
            print(company_data_dictionay)

            company_data_df = pd.DataFrame(company_data_dictionay)
            create_folder_path = f"/mnt/d/dataStorage/UPNepseDataLake/sshistoricNepseData/{company}_data"
            os.makedirs(create_folder_path,exist_ok=True)
            file_name = f"{company}.parquet"
            save_folder_path = os.path.join(create_folder_path,file_name)
            with open(os.path.join(logs_directory,'logs.txt'),'a') as log_file:
                log_file.write(f"successufully created file with name {file_name} at {create_folder_path}")
            company_data_df.to_parquet(save_folder_path,index=False)
        except Exception as e:
            with open(os.path.join(logs_directory,'logs.txt'),'a') as log_file:
                log_file.write(f"encountered error whille writing to file with name {save_folder_path} of  {company}")

                log_file.write(f"Error message : {e}")
                log_file.write(f" time : {datetime.now()}")

        else:
            with open(os.path.join(logs_directory,'logs.txt'),'a') as log_file:
                log_file.write(f"success in writing the data to {save_folder_path} of {company}")
                log_file.write(f" time : {datetime.now()}")



saving_files_to_datalake()

driver.quit()
