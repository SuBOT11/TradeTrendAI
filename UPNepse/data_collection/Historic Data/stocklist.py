import requests
from datetime import datetime, timedelta
import json
import pandas as pd
import os

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
    ret_url = f"https://www.merolagani.com/handlers/TechnicalChartHandler.ashx?type=get_advanced_chart&symbol={comp_symbol}&resolution=1D&rangeStartDate=1368490175&rangeEndDate={1702885413}&from=&isAdjust=1&currencyCode=NPR"
    res_from_lagani = requests.get(ret_url).json()
    for key,value in res_from_lagani.items():
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
    logs_directory= f"/mnt/d/dataStorage/UPNepseDataLake/historicNepseData/logs"
    list_comp = retrieve_comp()

    for company in list_comp:
        try:
            company_data_dictionay = retrieve_individual_histori_data(company)
            company_data_df = pd.DataFrame(company_data_dictionay)
            create_folder_path = f"/mnt/d/dataStorage/UPNepseDataLake/historicNepseData/{company}_data"
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
