import pandas as pd
import os

dframe = pd.read_parquet('/mnt/d/CollegeProject/UPNepse/data_load/data/NABIL.parquet')
print(dframe)

#dirs = "/mnt/d/CollegeProject/UPNepse/data_load/data"
#for file in os.listdir(dirs):
    #print(file)


