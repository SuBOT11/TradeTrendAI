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
from clean import write_to_database
options = webdriver.ChromeOptions()
options.set_capability("goog:loggingPrefs",{"performance":"ALL"})

service = Service(executable_path="./chromedriver")
driver = uc.Chrome(options=options,service=service)
driver.get_screenshot_as_file("screenshot.png")
load_dotenv()
username_ = os.getenv('USERNAME')
password_ = os.getenv('PASSWORD')
wait = WebDriverWait(driver, 5)

def login(username,password,url):
    driver.get(url)
    driver.get_screenshot_as_file("screenshot.png")
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


def write_data_to_file(file_name,data):
    date_n = datetime.now()
    date_nstr = date_n.strftime(f"%d_%B_%Y")
    create_folder_path = f"/mnt/d/CollegeProject/UPNepse/SastoShareScrape/daily_summary_ss/data/{date_nstr}"
    os.makedirs(create_folder_path,exist_ok=True)
    try:
        with open(os.path.join(create_folder_path,f"{file_name}_file.json"),'w') as bf:
            json.dump(data,bf,indent=2)
    except Exception as e:
        print("error writing data")
    else:
            print(f"success written time {datetime.now()}")



def extract_raw_data():

    fetch_url =  'https://nepsealpha.com/sastoshare/compare/index'
    driver.get(fetch_url)
    sleep(5)
    options_array = ['Development Banks','Finance','Commercial Banks','Hydro','Life Insurance','Microfinance']
    dropdown_xpath = ''
    #input_field = driver.find_element(By.XPATH,'//*[@id="vue_app_content"]/div/div/div[2]/div[1]/div/div/div/div/div/input')
    sleep(2)
    for option in options_array:
        print(option)
        try:
            input_field = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="vue_app_content"]/div/div/div[2]/div[1]/div/div/div/div/div/input' )))
            input_field.click()
            input_field.send_keys(option)
            input_field.send_keys(Keys.ARROW_DOWN)
            input_field.send_keys(Keys.ENTER)

    # Now you can interact with the element
        except:
            print("Element not found within 10 seconds.")

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
    list_of_keywords = ['DEVBANK','FINANCE','BANKING','HYDROPOWER','MICROFINANCE','LIFEINSU']
    records_dictionary = {}
    for log in filter(log_filter, logs):
        request_id = log["params"]["requestId"]
        resp_url = log["params"]["response"]["url"]
        if any(keyword in resp_url for keyword in list_of_keywords):
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



                write_data_to_file(file_name,{file_name:imp_data})

login(username_,password_,"https://nepsealpha.com/login")
extract_raw_data()
driver.quit()


write_to_database()
