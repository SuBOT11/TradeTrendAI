import json
from datetime import datetime
import pandas as pd
import pymongo
import os
from pymongo.errors import DuplicateKeyError

def mongo_connection(hostn,portn):
    try:
        client = pymongo.MongoClient(f'mongodb://{hostn}:{portn}')
        print("connection established ")
        return client
    except Exception as e:
        print(f'error occured {e} while connection was tried')


def cleaning_data():
    date_n = datetime.now()
    date_check = date_n.strftime(f"%Y-%m-%d")
    date_nstr = date_n.strftime(f"%d_%B_%Y")
    create_folder_path = f"/mnt/d/CollegeProject/UPNepse/SastoShareScrape/daily_summary_ss/data/{date_nstr}"
    save_loc  = '/mnt/d/CollegeProject/UPNepse/data_preparation/stock_data_preparation/daily_data'
    all_files = os.listdir(create_folder_path)
    cleaned_data_list =  []
    print(all_files)
    for files in all_files:
        with open(os.path.join(create_folder_path,f'{files}'),'r') as rf:
            raw_data_json = json.load(rf)
            for k,v in raw_data_json.items():
                data_list = v['data']
                for data in data_list:
                    cleaned_data_dic = {}
                    cleaned_data_dic['key'] = date_nstr
                    cleaned_data_dic['date'] = date_n
                    cleaned_data_dic['sector'] = data['sector']
                    cleaned_data_dic['symbol'] = data['symbol']
                    sym = data['symbol']
                    try:
                        with open(os.path.join(save_loc,f'{sym}.json'),'r') as ref:
                               daily_data_json = json.load(ref)
                               print(date_check , daily_data_json['Date'])
                               if date_check == daily_data_json['Date']:

                                    cleaned_data_dic['Close'] = daily_data_json['Close']
                                    cleaned_data_dic['Open'] = daily_data_json['Open']
                                    cleaned_data_dic['High'] = daily_data_json['High']
                                    cleaned_data_dic['Low'] = daily_data_json['Low']
                                    cleaned_data_dic['Volume'] = daily_data_json['Volume']
                                    cleaned_data_dic['Change'] = daily_data_json['Change']
                                    cleaned_data_dic['PC_Change']= daily_data_json['Pc_change']
                                    cleaned_data_dic['Pre_Close']= daily_data_json['prev_day_close']
                                    
                    except Exception as error:
                        print(f'Couldnt open the file for {sym} {error}')
                    cleaned_data_dic['full_name'] = data['stockinfo']['full_name']

                    cleaned_relative = data['realtive_value'].replace('\\"', '"')
                    cleaned_relative_dict = json.loads(cleaned_relative)
                    for key,value in cleaned_relative_dict.items():
                        cleaned_data_dic[key] = value


                    cleaned_general= data['general'].replace('\\"', '"')
                    cleaned_general_dict = json.loads(cleaned_general)
                    for key,value in cleaned_general_dict.items():
                        cleaned_data_dic[key] = value

                    cleaned_technical= data['technical'].replace('\\"', '"')
                    cleaned_technical_dict= json.loads(cleaned_technical)
                    for key,value in cleaned_technical_dict.items():
                        cleaned_data_dic[key] = value


                    cleaned_market = data['market_share'].replace('\\"', '"')
                    cleaned_market_dict= json.loads(cleaned_market)
                    for key,value in cleaned_market_dict.items():
                        cleaned_data_dic[key] = value


                    cleaned_profit = data['profitability'].replace('\\"', '"')
                    cleaned_profit_dict= json.loads(cleaned_profit)
                    for key,value in cleaned_profit_dict.items():
                        cleaned_data_dic[key] = value

                    cleaned_data_list.append(cleaned_data_dic)

    return cleaned_data_list

def write_to_database():
    db = mongo_connection("172.18.0.2","27017")['ss_summary_db']

    if 'summary' in db.list_collection_names():
    # Select the collection
        collection = db['summary']

    # Drop the collection
        collection.drop()
    data_list = cleaning_data()

    try:
        summary_coll = db['summary']
        result = summary_coll.insert_many(data_list)
        print("Document inserted:", result.inserted_ids)
    except DuplicateKeyError:
        print("Duplicate key error: Document not inserted")


# Close connection to MongoDB

if __name__ == "__main__":
    write_to_database()


