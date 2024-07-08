import pandas as pd 
import json
import os
import nepali_datetime

def convert_date(fs_year):
    years = fs_year.split('/')
    start_year = int(f"{years[1]}")
    start_year_month = 4
    start_year_day = 1


    str_end_year  =str(int(years[1]) + 1 )
    end_year = int(f"{str_end_year}")
    end_year_month = 3
    end_month_day = 31

    start_date = nepali_datetime.date(start_year,start_year_month,start_year_day).to_datetime_date()
    end_date = nepali_datetime.date(end_year,end_year_month,end_month_day).to_datetime_date()
    return ([start_date,end_date])

    


def extract_dividend_info(dir_path):

    indexing = { }

    if not os.path.exists(os.path.join(dir_path,'dividend_file.json')):
        return
    with open(os.path.join(dir_path,'dividend_file.json'),'r') as fd:
        my_set = set()
        raw_data = json.load(fd)
        try:
            financial_json = raw_data['dividend']['dividend']
        except Exception as e:
            return 
        if (not len(financial_json) >= 1) or (not isinstance(financial_json,list)):
            return 1
        symbol_d = ''
        for data in financial_json:
            #data_json = {}
            my_set.add(data['fiscal_year'])
            
        data_json_arr  = [] 
        for fs in my_set:
            data_json= {}
            for data in financial_json:
                if data['fiscal_year'] == '0':
                    continue
                symbol_d = data['symbol']
                if fs == data['fiscal_year']:
                    if indexing.get(data['fiscal_year']):
                       date_converted = indexing.get(data['fiscal_year']) 
                    else:
                       date_converted = convert_date(data['fiscal_year'])
                       indexing[data['fiscal_year']] = date_converted
                    data_json['fiscal_year'] = data['fiscal_year']
                    data_json['start_date']= date_converted[0]
                    data_json['end_date'] = date_converted[1]
                    data_json['symbol'] = data['symbol']
                    data_json['book_closure_date'] = data['book_closure_date']
                    data_json['bonus_dividend'] = data['bonus_dividend']
                    data_json['cash_dividend'] = data['cash_dividend']
                    data_json['dividend_growth_rate'] = data['dividend_growth_rate']
            data_json_arr.append(data_json)

        financial_df = pd.DataFrame(data_json_arr) 
        save_dir = f'/mnt/d/CollegeProject/UPNepse/data_preparation/dividend_data_transform/data/{symbol_d}'
        os.makedirs(save_dir,exist_ok=True)
        print(save_dir)
        financial_df.to_json(f'{save_dir}/dividend.json')
    



def save_folder():
    data_path  = '/mnt/d/dataStorage/UPNepseDataLake/historicFinancialData/'
    folders = os.listdir(data_path)
    for folder in folders:
        print(folder)
        extract_dividend_info(os.path.join(data_path,folder))

save_folder()