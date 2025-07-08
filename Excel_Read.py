import pandas as pd
import os

PATH='D:/Python_projects/'
in_file="/BSM_Data.xlsx"

def import_excel(path=PATH,col="BMS ID"):
    path = os.path.join(path,in_file)
    df = pd.read_excel(path)
    bms_id = df[col].to_list()
    return bms_id

def export_excel(dict,path=PATH):
    df =pd.DataFrame(list(dict.items()),columns=['BSM_ID','BUSINESS_NAME'])
    df.to_excel("Results.xlsx",index=False)