from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import bs4
import pandas as pd
import re

cari= input("keyword pencarian:")
hal= input("berapa halaman:")
nama_file= input("nama file(sertakan.csv):")

#webdriver option
opt= webdriver.ChromeOptions()
opt.add_argument('--no-sandbox')
opt.add_argument('--headless')
opt.add_argument('--disable-notifications')
opt.add_argument('--disable-infobars')

#basic code
driver = webdriver.Chrome(executable_path='D:\Github\coba\chromedriver.exe',options=opt)
driver.get('https://shopee.co.id/')
time.sleep(1)

#search
search = driver.find_element(By.XPATH,'//*[@id="main"]/div/header/div[2]/div/div[1]/div[1]/div/form/input')
search.send_keys(cari)
search.send_keys(Keys.ENTER)
time.sleep(5)

#terlaris
# terlaris = driver.find_element(By.XPATH,'//*[@id="main"]/div/div[2]/div/div/div[2]/div[3]/div[1]/div[1]/div[3]')
# terlaris.click()
# time.sleep(1)

# zoom out
driver.execute_script("document.body.style.zoom='10%'")
time.sleep(2)

# variabel kosong untuk menampung data html
data=str()

# paginasi
for k in range (int(hal)) :
    #ambl semua data di page tsb
    data += driver.page_source
    time.sleep(5)
    # navigasi ke page selanjutnya
    next = driver.find_element(By.CSS_SELECTOR,' button.shopee-icon-button.shopee-icon-button--right ')
    driver.execute_script("arguments[0].click();", next)
    time.sleep(5)        
    
driver.close()

# parse semua data masing masing produk
soup = bs4.BeautifulSoup(data)
all_product = soup.find_all('div',{'class':"col-xs-2-4 shopee-search-item-result__item"})

# variabel kosong untuk menyatukan data
data_dict_list = []

#menata dan merapikan data ke masing masing index
for product in all_product:
    title_element = product.find('div',{'class':'ie3A+n bM+7UW Cve6sh'})
    title_text = title_element.text

    price_element = product.find('div',{'class':'hpDKMN'})
    price_text = price_element.text

    #gunakan if-else jika terdapat data yang kosong
    # pricedc_element = product.find('span',{'class':'ZEgDH9'})
    # if pricedc_element is None:
    #     pricedc_text = None
    # else:
    #     pricedc_text = pricedc_element.text
    
    terjual_element = product.find('div',{'class':'r6HknA uEPGHT'})
    if terjual_element is None:
        terjual_text = None
    else:
        terjual_text = terjual_element.text
    
    product_link_element = product.find('a')
    product_link = product_link_element.get('href')
    
    #gabung data dalam dict()
    data_dict = dict()
    data_dict['title'] = title_text
    data_dict['price'] = price_text
    # data_dict['pricedc'] = pricedc_text
    data_dict['sales'] = terjual_text
    data_dict['link'] = product_link
    data_dict_list.append(data_dict)

#ubah ke dalam dataframe menggunkan pandas    
data_df = pd.DataFrame(data_dict_list)

#bersihkan harga
def clean_price(price):
    result = re.findall(r'[0-9.,]+',price)
    if '-' in price:
        original_price = None
        min_price = result[0]
        max_price = result[1]
    elif len(result) == 2:
        original_price = result[0]
        min_price = result[1]
        max_price = result[1]
    elif len(result) == 1:
        original_price = result[0]
        min_price = result[0]
        max_price = result[0]
        
    price_list =  [original_price,min_price,max_price]
    price_clean_list = []
    for price in price_list:
        if price is None:
            price_clean_list.append(None)
        else:
            price_clean_list.append(int(price.replace('.','')))
    
    return price_clean_list

price_clean_ser = data_df['price'].apply(clean_price)
price_clean_df = pd.DataFrame(price_clean_ser)
price_clean_list = list(price_clean_ser)
price_clean_df = pd.DataFrame(price_clean_list, columns=['Original Price', 'Min Price', 'Max Price'])
price_data_df = pd.concat([data_df,price_clean_df],axis=1)

#drop price dan eksport csv
new = price_data_df.drop(['price'],axis=1)
new.to_csv(nama_file,index=False,sep=';')