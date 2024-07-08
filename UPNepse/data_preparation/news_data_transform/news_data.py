
import pandas as pd 
import json
import os
import nepali_datetime


    


whole_symbols = []
def extract_news_info(dir_path,fold):
    s_name = fold.split('_')[0]

    print(s_name)

    whole_news_dic = {}
    indexing = { }
    with open(os.path.join(dir_path,'corporate_action_file.json'),'r') as fd:
        whole_news_dic = {}
        json_data = json.load(fd)
        date_arr = []
        try:
            data = json_data['corporate_action']['news']
            for k,v in data.items():
                date_arr.append(k)

            for k,v in json_data['corporate_action']['announcements'].items():
                date_arr.append(k)

            info = json_data['corporate_action']['stockInfo']
            stock = info[0]['symbol']

            whole_news_dic[stock]  =   date_arr 
        except Exception as e:
            date_arr.append('2018-01-01')
            whole_news_dic[s_name] = date_arr

            print("Exception"+ s_name)
    
    whole_symbols.append(whole_news_dic)


     



    save_dir = f'/mnt/d/CollegeProject/UPNepse/data_preparation/news_data_transform/data'
    os.makedirs(save_dir,exist_ok=True)
        #print(save_dir)
    with open(os.path.join(save_dir,'news.json'),'w') as rf:
        json.dump(whole_symbols,rf)
    



def save_folder():
    data_path  = '/mnt/d/dataStorage/UPNepseDataLake/historicFinancialData/'
    folders = os.listdir(data_path)
    for folder in folders:
        extract_news_info(os.path.join(data_path,folder),folder)
    
    print(whole_symbols)

save_folder()