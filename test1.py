import requests
import pandas as pd
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

#webdriver option
opt= webdriver.ChromeOptions()
opt.add_argument('--no-sandbox')
opt.add_argument('--headless')
opt.add_argument('--disable-notifications')
opt.add_argument('--disable-infobars')

path='D:\Github\coba\chromedriver.exe'

driver= webdriver.Chrome(executable_path=path,options=opt)

data_dict_list = []

for page in range (0,2):
    main_link = 'https://shopee.co.id/search?keyword=skincare&page={}'.format(page)
    driver.get(main_link)
    driver.execute_script("document.body.style.zoom='10%'")
    data = driver.page_source
    soup = bs4.BeautifulSoup(data)
    all_product = soup.find_all('div',{'class':"col-xs-2-4 shopee-search-item-result__item"})
    
    for product in all_product:
        title_element = product.find('div',{'class':'ie3A+n bM+7UW Cve6sh'})
        title_text = title_element.text

        price_element = product.find('div',{'class':'hpDKMN'})
        price_text = price_element.text

        sales_element = product.find('div',{'class':'r6HknA uEPGHT'})
        if sales_element is None:
            sales_text = None
        else:
            sales_text = sales_element.text

        product_link_element = product.find('a')
        product_link = product_link_element.get('href')
    
        data_dict = dict()
        data_dict['title'] = title_text
        data_dict['price'] = price_text
        data_dict['sales'] = sales_text
        data_dict['link'] = product_link
        data_dict_list.append(data_dict)
   
data_df = pd.DataFrame(data_dict_list)
print(data_df)