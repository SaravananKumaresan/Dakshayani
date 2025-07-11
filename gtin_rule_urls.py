import os
import pandas as pd

IN_PATH='D:/Python_projects/'
in_file="GDSN_details.xlsx"

URL = ['https://www.gs1.org/1/gtinrules/en/rule/264/new-product-introduction',
        'https://www.gs1.org/1/gtinrules/en/rule/263/declared-formulation-or-functionality',
        'https://www.gs1.org/1/gtinrules/en/rule/266/declared-net-content',
        'https://www.gs1.org/1/gtinrules/en/rule/265/dimensional-or-gross-weight-change',
        'https://www.gs1.org/1/gtinrules/en/rule/267/add-or-remove-certification-mark',
        'https://www.gs1.org/1/gtinrules/en/rule/268/primary-brand',
        'https://www.gs1.org/1/gtinrules/en/rule/269/time-critical-or-promotional-product',
        'https://www.gs1.org/1/gtinrules/en/rule/270/packcase-quantity',
        'https://www.gs1.org/1/gtinrules/en/rule/271/predefined-assortment',
        'https://www.gs1.org/1/gtinrules/en/rule/272/price-on-pack']


def import_excel(cols,fname=in_file,path=IN_PATH,sheet_name='3.1.31'):
    bmsid_with_def={}
    path = os.path.join(path,fname)
    df = pd.read_excel(path,sheet_name=sheet_name)
    var_1 = df[cols[0]].to_list()
    var_2 = df[cols[1]].fillna(" ").to_list()
 
    for i in range(len(var_1)):
        bmsid_with_def[var_1[i]]= var_2[i]
    return bmsid_with_def



def export_excel(d,fname,cols,path=IN_PATH):
    df =pd.DataFrame(list(d.items()),columns=cols)
    df.to_excel(fname,index=False)


