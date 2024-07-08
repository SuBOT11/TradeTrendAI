from time import sleep
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import requests
import re
from selenium.webdriver.chrome.service import Service
from datetime import datetime

options = webdriver.ChromeOptions()
options.add_argument('--headless')
service = Service(executable_path="/usr/local/bin/chromedriver")
driver = webdriver.Chrome(options=options,service=service)

url = "https://www.sharesansar.com/floorsheet"
driver.get(url)

select_field = driver.find_element(By.XPATH,'//*[@id="select2-company-container"]')
sleep(2)
select_field.click()
sleep(2)
list_of_comp = driver.find_element(By.XPATH,'//*[@id="select2-company-results"]')
companies = list_of_comp.find_elements(By.TAG_NAME,"li")

needed_dict = {}  
pattern = re.compile(r'\S / \S')
for company in companies:
    name =  company.text
    if pattern.search(name):

        com_arr = name.split(' / ')
        needed_dict[com_arr[1]] = com_arr[0]

comp_dict = {}
with open('active_comp.json','r') as acc:
    comp_dict = json.load(acc)


for k in comp_dict.keys():
    if k in needed_dict.keys():
        print("matched stock \n")
        print(f"{needed_dict[k]} and {comp_dict[k]}") 
        comp_dict[k] =  needed_dict[k] 


with open('active_comp.json','w') as of:
    json.dump(comp_dict,of)


driver.close()
    





