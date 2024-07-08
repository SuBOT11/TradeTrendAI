
import os
import warnings
import numpy as np 
import pandas as pd
import pandas_ta as ta
import json

def only_active_comp():

    companies = []
    with open('/mnt/d/CollegeProject/UPNepse/data_collection/active_comp.json','r') as rf:
        comp_data = json.load(rf)
        for k,v in comp_data.items():
            companies.append(k)
    return companies     
    
only_active_comp()
def add_indicators(df):
    print(df)
    df['Volume'] = df['Volume'].astype(float)
    df['SMA_20'] = ta.sma(df['Close'],length=20)
    df['SMA_100'] = ta.sma(df['Close'],length=100)
    df['EMA_20'] = ta.ema(df['Close'],length=20)
    df['EMA_100'] = ta.ema(df['Close'],length=100)
    df['RSI_14'] = ta.rsi(df['Close'],length=14)
    df['ROC_12']  = ta.roc(df['Close'],length=12)
    df['ATR_14'] = ta.atr(df['High'],df['Low'],df['Close'],length=14)
    df['SD_20'] = ta.stdev(df['Close'], length=20)
    df['OBV'] = ta.obv(df['Close'], df['Volume'])
    try:
        df['ADX_14'] = ta.adx(df['High'],df['Low'],df['Close'],length=14)['ADX_14']
    except Exception as e:
        print(e,"sorry adx")
        df['ADX_14']  = 0


def read_files():

    companies = only_active_comp()
    folder_path = '/mnt/d/dataStorage/UPNepseDataLake/sshistoricNepseData'

    save_location = '/mnt/d/CollegeProject/UPNepse/data_preparation/stock_data_preparation/data'

    os.makedirs(save_location,exist_ok=True)
    data_already_present = os.listdir(save_location)
    if len(data_already_present) > 0:
        for file in data_already_present:

            df = pd.DataFrame()
            df = pd.read_parquet(os.path.join(save_location,file))
            new_rows_df = pd.DataFrame()
            try:
                file_ar = file.split('.')
                f_name = file_ar[0]
                with open(f'/mnt/d/CollegeProject/UPNepse/data_preparation/stock_data_preparation/daily_data/{f_name}.json','r') as rf:
                    json_data = json.load(rf)
                    json_data_mod = {}
                    for key,val in json_data.items():
                        if key in ['Date','Close','Open','High','Low','Volume']:
                            json_data_mod[key] = val
                    print(json_data_mod)
                    new_rows_df = pd.DataFrame([json_data_mod])
            except Exception as err:
                print("sorry")

            if not new_rows_df.empty:
                df = pd.concat([df, new_rows_df], ignore_index=True)
                print(df.tail())
            add_indicators(df)
            df.to_parquet(f'{save_location}/{f_name}.parquet',overwrite=True)
    else:

        os.makedirs(save_location,exist_ok=True)
        for folder in companies:
            st_folder  = f"{folder_path}/{folder}_data"
            files = os.listdir(st_folder)

            for file_n in files:
                df = pd.DataFrame()
                df = pd.read_parquet(os.path.join(st_folder,file_n))
                new_rows_df = pd.DataFrame()
                try:
                    with open(f'/mnt/d/CollegeProject/UPNepse/data_preparation/stock_data_preparation/daily_data/{folder}.json','r') as rf:
                        json_data = json.load(rf)
                        json_data_mod = {}
                        for key,val in json_data.items():
                            if key in ['Date','Close','Open','High','Low','Volume']:
                                json_data_mod[key] = val
                        print(json_data_mod)
                        new_rows_df = pd.DataFrame([json_data_mod])
                except Exception as err:
                    print("sorry")

                if not new_rows_df.empty:
                    df = pd.concat([df, new_rows_df], ignore_index=True)
                    print(df.tail())
                add_indicators(df)
                df.to_parquet(f'{save_location}/{folder}.parquet')

            


read_files()