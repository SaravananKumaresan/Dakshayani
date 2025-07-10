import pytest
from selenium import webdriver
from selenium .webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
import os,re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from datetime import datetime
from Excel_Read import import_excel,export_excel

EDGE_DRIVER_PATH = 'D:/Python_projects/Driver/msedgedriver.exe'
URL = 'https://navigator.gs1.org/'
NO_RECORDS = "Loaded 0/0 results"
out_dict={}

bmi_id = import_excel()

@pytest.fixture
def driver_init():
    service = Service(executable_path= EDGE_DRIVER_PATH)
    options = webdriver.EdgeOptions()
    options.add_argument("start-maximized")
    options.add_argument("log-level=3")
    driver = webdriver.Edge(service=service,options=options)
    yield driver
    driver.quit()


def test_gdm_scrap(driver_init):
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_name = os.path.join("D:/Python_projects/",f"{date_str}_run.log")
    logging.basicConfig(
    filename=file_name,level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",force=True)
    url = URL
    driver_init.get(url)
    gs1_gdm_link = WebDriverWait(driver_init,10).until(
        EC.presence_of_element_located((By.XPATH,"//*[@id='app']/div/div[2]/div/section[2]/div/div/div[1]"))
        )
    gs1_gdm_link.click()
    qs = WebDriverWait(driver_init,10).until(
        EC.presence_of_element_located((By.XPATH,"//*[@id='app']/div/div[2]/div[2]/section[2]/div/div/div[1]"))
        )
    qs.click()
    for bid in bmi_id:
        try:
            sb = WebDriverWait(driver_init,10).until(
                EC.presence_of_element_located((By.XPATH,"//*[@id='app']/div/div[2]/div[2]/section[2]/div/div[1]/div/div/div/input"))
                )
            sb.clear()
            sb.send_keys(bid)
            time.sleep(5)
            search = WebDriverWait(driver_init,10).until(
                EC.presence_of_element_located((By.XPATH,"//*[@id='app']/div/div[2]/div[2]/section[2]/div/div[1]/div/div/div/i[2]"))
                )
            time.sleep(5)
            search.click()

            tot_record_ele =  WebDriverWait(driver_init,10).until(
                EC.element_to_be_clickable((By.XPATH,"//*[@id='app']/div/div[2]/div[2]/section[2]/div/div[3]/div/div/table/tfoot/tr/td/span"))
                )
            if  tot_record_ele.text != NO_RECORDS:

                result = WebDriverWait(driver_init,10).until(
                    EC.element_to_be_clickable((By.XPATH,"//*[@id='app']/div/div[2]/div[2]/section[2]/div/div[3]/div/div/table/tbody/a[1]"))
                    )
                texts = driver_init.find_element(By.XPATH,"//*[@id='app']/div/div[2]/div[2]/section[2]/div/div[3]/div/div/table/tbody/a[1]/td[1]").text
                if int(texts) == bid:
                    driver_init.execute_script("arguments[0].scrollIntoView({behaviour: 'smooth',block:'center'});",result)
                    driver_init.execute_script("arguments[0].click();",result)

                b_name_ele = WebDriverWait(driver_init,20).until(
                    EC.element_to_be_clickable((By.XPATH,"//*[@id='app']/div/div[2]/div[2]/section[2]/div/div[2]/div/div[1]/div[1]/ul/li[1]/span[1]"))
                    )
                b_name = driver_init.find_element(By.XPATH,"//*[@id='app']/div/div[2]/div[2]/section[2]/div/div[2]/div/div[1]/div[1]/ul/li[1]/span[2]").text
    
                if not b_name:
                    try:
                        t_name = WebDriverWait(driver_init,20).until(
                        EC.element_to_be_clickable((By.XPATH,"//*[@id='app']/div/div[2]/div[2]/section[2]/div/div[2]/div/div[1]/div[2]/ul/li[1]/span[2]"))
                        )
                        t_name =re.sub(r'(?<!^)(?=[A-Z])',' ',t_name.text)
                        out_dict[bid]=t_name
                        logging.info(f"{str(bid).zfill(4)} | PASSED: {str(t_name)}")
                    except :
                        out_dict[bid]='NO Tname and no Bname'
                        logging.info(f"{str(bid).zfill(4)} | PASSED: {str("NO Tname and no Bname")}")
                        go_back_btn = WebDriverWait(driver_init,20).until(
                        EC.element_to_be_clickable((By.XPATH,"//*[@id='goBackButton']"))
                        )
                        go_back_btn.click()                      
                else:
                    out_dict[bid]=b_name
                    logging.info(f"{str(bid).zfill(4)} | PASSED: {str(b_name)}")
                go_back_btn = WebDriverWait(driver_init,20).until(
                    EC.element_to_be_clickable((By.XPATH,"//*[@id='goBackButton']"))
                    )
                go_back_btn.click()                   
            else:
                out_dict[bid]="No results"
                logging.info(f"{str(bid).zfill(4)} | PASSED: Zero results")
        except Exception as e:
             logging.error(f"{str(bid).zfill(4)} | FAILED: {str(e)}")
            

def test_export():
    export_excel(out_dict)