from time import sleep
import re
import os
from datetime import datetime
import json
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
driver = webdriver.Chrome(options=options,service=service)
url = "https://www.sharesansar.com/floorsheet"



company_name_list = []
active_date_list = []
def retrieve_active_company():
    with open('/mnt/d/CollegeProject/UPNepse/data_collection/active_comp.json','r') as comp_data:
        com_data = json.load(comp_data)
        #co_pattern = re.compile(r'\bCo(?:\.|\b)',re.IGNORECASE)
        #ltd_pattern = re.compile(r'\bLtd(?:\.|\b)',re.IGNORECASE)
        #for k,v in com_data.items():
        #    co_matches_sub = co_pattern.sub("Company",v)

        #    com_data[k] = co_matches_sub

        #    ltd_matches_sub = ltd_pattern.sub("Limited",com_data[k])
        #    com_data[k] = ltd_matches_sub

        for k,v in com_data.items():
            formatted_string =  f"{v} / {k}"
            company_name_list.append(formatted_string)




def retrieve_active_date():
    with open('/mnt/d/CollegeProject/UPNepse/utility_data_file/active_date.json','r') as date_file:
        data_date = json.load(date_file)
        for date in data_date:
            print(date)
            active_date_list.append(date)
retrieve_active_date()
retrieve_active_company()
def search_the_data(company,date_arr):

    for a_date in date_arr:
        print(a_date, company)
        check_path = f"/mnt/d/dataStorage/UPNepseDataLake/historicBrokerData/{company}_broker_data/{a_date}_file.json"
        check_folder_dir = f"/mnt/d/dataStorage/UPNepseDataLake/historicBrokerData/{company}_broker_data/2023-12-19_file.json"
        if os.path.exists(check_folder_dir):
            print(f"all files fetched for {company} stock date")
            continue
        if os.path.exists(check_path):
            print(f"already file is present for {company} in {a_date} ")
            continue




        form_element = driver.find_element(By.XPATH,'//*[@id="frm_floorsheet"]')

        date_field = form_element.find_element(By.XPATH,'//*[@id="date"]')
        date_field.clear()
        date_field.send_keys(a_date)

        sleep(2)

        company_insert_field = form_element.find_element(By.XPATH,'//*[@id="frm_floorsheet"]/div[1]/span/span[1]/span')


        company_insert_field.click()


        sleep(2)

        com_input_field_el  =  form_element.find_element(By.XPATH,'/html/body/span/span/span[1]/input')
        com_input_field_el.send_keys(company)
        com_input_field_el.send_keys(Keys.RETURN)


        sleep(5)
        submit_btn = driver.find_element(By.XPATH,'//*[@id="btn_flsheet_submit"]')
        submit_btn.click()


        my_table_wrapper_element = driver.find_element(By.XPATH,'//*[@id="myTable_wrapper"]')
        total_entries_selection_element = Select(driver.find_element(By.XPATH,'//*[@id="myTable_length"]/label/select'))
        #next_btn_element = driver.find_element(By.XPATH,'//*[@id="myTable_next"]')
        total_entries_selection_element.select_by_index(3)

        sleep(4)


        time = 10
        while time > 0 :
            wait = WebDriverWait(driver,10)

            next_btn_element = driver.find_element(By.XPATH,'//*[@id="myTable_paginate"]')
            next_el = next_btn_element.find_element(By.ID,'myTable_next')
            try:
                next_btn = wait.until(EC.element_to_be_clickable(next_el))
                driver.execute_script("arguments[0].click();", next_btn)
                print("button clicked ")
                time = time - 1
                sleep(1)

            except:
                print("failed to click button exiting ")
                break

            finally:
                break



        table_with_rows = driver.find_element(By.XPATH,'//*[@id="myTable"]')
        rows = table_with_rows.find_elements(By.XPATH,'//*[@id="myTable"]/tbody/tr')
        if len(rows) < 2 :
            create_folder_path = f"/mnt/d/dataStorage/UPNepseDataLake/historicBrokerData/{company}_broker_data"
            create_logs_folder_path = f"/mnt/d/dataStorage/UPNepseDataLake/Broker_logs_data/{company}_logs_data"
            os.makedirs(create_folder_path,exist_ok=True)
            os.makedirs(create_logs_folder_path,exist_ok=True)
            with open(os.path.join(create_folder_path,f"{a_date}_file.json"),'w') as bf:
                json.dump({"data":"nothing on this date"},bf,indent=2)
            continue
        sleep(4)

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
            print(f"Caught {resp_url}")
            resp_json_from_net = (driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id}))
            imp_data = {}
            json_resp = json.dumps(resp_json_from_net)
            json_resp_dict = json.loads(json_resp)
            for k,v in json_resp_dict.items():
                if k == "body":
                    imp_data = json.loads(v)
                    print(imp_data)

            records_dictionary[resp_url] = imp_data
            sleep(3)
        for k,v in records_dictionary.items():
            print(f"k \n")
        print("Successfully fetched from the  web \n")
        create_folder_path = f"/mnt/d/dataStorage/UPNepseDataLake/historicBrokerData/{company}_broker_data"
        create_logs_folder_path = f"/mnt/d/dataStorage/UPNepseDataLake/Broker_logs_data/{company}_logs_data"
        os.makedirs(create_folder_path,exist_ok=True)
        os.makedirs(create_logs_folder_path,exist_ok=True)
        try:
            with open(os.path.join(create_folder_path,f"{a_date}_file.json"),'w') as bf:
                json.dump(records_dictionary,bf,indent=2)
        except Exception as e:
            with open(os.path.join(create_logs_folder_path,f"{a_date}_error_log_file.txt"),'w') as ef:
                ef.write(f"encountered error while writing to {company} data of date : {a_date} \n")
                ef.write(f"{e} /n")
                ef.write(f"error time {datetime.now()}")
        else:
            with open(os.path.join(create_logs_folder_path,f"{a_date}_log_file.txt"),'w') as ef:
                ef.write(f"successfully written to {company} data of date : {a_date} \n")
                ef.write(f"success written time {datetime.now()}")



        sleep(1)

        driver.refresh()

        sleep(1)
    return 1

def saving_files_to_datalake():
    date_last_200 = active_date_list[-200:]

    for company in company_name_list:
        key_word = search_the_data(company,date_last_200)
        logs_folder = f"/mnt/d/dataStorage/UPNepseDataLake/Broker_logs_data/{company}_logs_data/final_log"
        os.makedirs(logs_folder,exist_ok=True)
        if key_word == 1:
            print(f"successfully written data of {company} to the datalake ")
            with open(os.path.join(logs_folder,"final.txt"),"w") as fin_l:
                fin_l.write(f"successfully written broker data at {datetime.now()} ")
        else:
            print(f"failed to written data of {company} to the datalake ")
            with open(os.path.join(logs_folder,"error_final.txt"),"w") as fin_l:
                fin_l.write(f"failed to write broker data at {datetime.now()} ")




driver.get(url)
sleep(2)
saving_files_to_datalake()
driver.quit()
