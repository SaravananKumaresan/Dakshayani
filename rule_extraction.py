from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium .webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os,re,pytest,copy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gtin_rule_urls
from gtin_rule_urls import import_excel,export_excel

URLS=gtin_rule_urls.URL
PATH_RULES = gtin_rule_urls.IN_PATH


EDGE_DRIVER_PATH = 'D:/Python_projects/Driver/msedgedriver.exe'
rules={}

bmsid_def = import_excel(['BMSid','Definition'])

@pytest.fixture
def driver_init():
    service = Service(executable_path= EDGE_DRIVER_PATH)
    options = webdriver.EdgeOptions()
    options.add_argument("start-maximized")
    options.add_argument("log-level=3")
    driver = webdriver.Edge(service=service,options=options)
    yield driver
    driver.quit()
    
    
def test_drivers(driver_init):
    global rules
    if not (os.path.exists(os.path.join(PATH_RULES,'gsdn_rules.xlsx'))): 
        for url in URLS:    
            extract_gtin_rule(driver_init,url)
            time.sleep(1)
        export_excel(rules,'gsdn_rules.xlsx',['RULE_NAME','RULE_DEF'])
        
    else:
        rules_dict=import_excel(['RULE_NAME','RULE_DEF'],'gsdn_rules.xlsx',PATH_RULES,sheet_name='Sheet1')
        rules=copy.deepcopy(rules_dict)
    
    s_transform()
        
        
        
        
        
    
    
    
def extract_gtin_rule(driver_init,url):
    driver_init.get(url)
    WebDriverWait(driver_init,20).until(
    EC.presence_of_element_located((By.XPATH,'//*[@id="skip-link"]/div[1]/div/section/div/div[2]/div/div[1]/div[2]'))
    )
    
    tot_record_ele =  WebDriverWait(driver_init,10).until(
                EC.element_to_be_clickable((By.XPATH,'//*[@id="skip-link"]/div[1]/div/section/div/div[2]/h2'))
                )
    rule_name = tot_record_ele.text
    soup = BeautifulSoup(driver_init.page_source,'html.parser')

    rule_container = soup.find('div',class_ = 'col-md-12')
    if rule_container:
        text=rule_container.find('p')
        if text:
            para=text.get_text(strip=True)
            rules[rule_name]=para
        else:
            print('Empty')
    
    
    
def s_transform():
    pass    

       
    
