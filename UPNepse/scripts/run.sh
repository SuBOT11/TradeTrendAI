#!/bin/bash

usr/bin/python3 /mnt/d/CollegeProject/UPNepse/data_collection/Daily_Data_Fetch/get_daily_stock_info.py
usr/bin/python3 /mnt/d/CollegeProject/UPNepse/data_preparation/stock_data_preparation/prepare_stock_data.py



~/anaconda3/envs/data_prep/bin/python /mnt/d/CollegeProject/UPNepse/MLmodel/rnn_lstm.py

