from time import sleep
import json
from selenium import webdriver

from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
options.set_capability("goog:loggingPrefs",{"performance":"ALL"})
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service,options=options)
url = "https://nepsealpha.com/trading/chart?symbol=UPPER"

driver.get(url)
sleep(30)

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
    print(f"Caught {resp_url}")
    #print(driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id}))

sleep(20)

driver.quit()