import requests
import json

def retrieve_comp():

    url = "https://eng.merolagani.com/handlers/AutoSuggestHandler.ashx?type=Company"
    res = requests.get(url).json()
    company_list = []
    for r in res:
        incorrect_name = r['l']
        split1 = (incorrect_name.split(maxsplit=1))
        symbol = split1[0]
        full_name_un = split1[1]
        full_name = full_name_un[1:-1]
        required_name = f"{full_name} / {symbol}"
        company_list.append(required_name)
    with open("formatted_comp_name.txt",'w') as c_file:
        json.dump(company_list,c_file)


def active_company_list():
    url = ''
