from time import sleep
import pytz
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import requests
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from pytz import timezone

npt = timezone('Asia/Katmandu')

def get_active_comp_list():
    active_company_dict = {}
    options = webdriver.ChromeOptions()
    options.set_capability("goog:loggingPrefs",{"performance":"ALL"})
    #options.add_argument("--headless=old")
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(options=options)
    url = "https://www.nepalstock.com/company"

    driver.get(url)
    sleep(2)



    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

    def log_filter(log_):
        return (
            # is an actual response
            log_["method"] == "Network.responseReceived"
            # and json
            and "json" in log_["params"]["response"]["mimeType"]
        )

    for log in filter(log_filter, logs):

        request_id = log["params"]["requestId"]
        resp_url = log["params"]["response"]["url"]
        if resp_url == 'https://www.nepalstock.com/api/nots/securityDailyTradeStat/58':
            resp_json_from_net = (driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id}))
            json_resp = json.dumps(resp_json_from_net)
            json_resp_dict = json.loads(json_resp)
            for k,v in json_resp_dict.items():
                if k == "body":
                    imp_data =json.loads(v)
                    for data in imp_data:
                        data["symbol"] = data["securityName"]


    sleep(2)
    with open('active_comp.json','w') as tdf:
        json.dump(active_company_dict,tdf)

    driver.quit()

def get_active_date():
    new_stockdate_list= []
    ret_url = 'https://eng.merolagani.com/handlers/TechnicalChartHandler.ashx?type=get_advanced_chart&symbol=NEPSE&resolution=1D&rangeStartDate=1670648809&rangeEndDate=1704776869&from=&isAdjust=1&currencyCode=NPR'
    res_from_lagani = requests.get(ret_url).json()
    for key,value in res_from_lagani.items():
        if key == 't':
            for ts in value:
                new_time_obj = datetime.utcfromtimestamp(ts).replace(tzinfo=pytz.utc)
                formatted_datetime_obj = new_time_obj.strftime("%Y-%m-%d")
                new_stockdate_list.append(formatted_datetime_obj)
                print(formatted_datetime_obj)

    with open('active_date_2.json','w') as date_json_file:
        json.dump(new_stockdate_list,date_json_file)

get_active_date()