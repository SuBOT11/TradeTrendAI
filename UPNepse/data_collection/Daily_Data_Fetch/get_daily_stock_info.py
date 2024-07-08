import requests
import json 
from datetime import datetime
import os
import pandas as pd

url  = 'https://www.nepalipaisa.com/api/GetStockLive'
response = requests.get(url).json()
stock_list = response['result']['stocks']
save_loc  = '/mnt/d/CollegeProject/UPNepse/data_preparation/stock_data_preparation/daily_data'
os.makedirs(save_loc,exist_ok=True)


for stock in stock_list:
    stock_dic = {}
    symbol = stock['stockSymbol']
    stock_dic['Date'] = stock['tradeDate']
    stock_dic['Close'] = stock['closingPrice']
    stock_dic['Open'] = stock['openingPrice']
    stock_dic['High'] = stock['maxPrice']
    stock_dic['Low'] = stock['minPrice']
    stock_dic['Volume'] = stock['volume']
    stock_dic['Change']  = stock['differenceRs']
    stock_dic['Pc_change'] = stock['percentChange']
    stock_dic['prev_day_close'] = stock['previousClosing']

    try:
        with open(os.path.join(save_loc,f'{symbol}.json'),'w') as wf:
            json.dump(stock_dic,wf)

    except Exception as e:
        print("sorry")
        continue


