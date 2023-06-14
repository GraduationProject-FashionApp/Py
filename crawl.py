from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.request
import time
import os
import csv

folder_path = 'D:\\GraduationProject-Team3\\testImage'
f = open("D:\\GraduationProject-Team3\\dataCrawl.csv", 'w', newline="", encoding='utf-8-sig')
writer = csv.writer(f)
print("Type searchTag")
searchTag = input()
arrayItem = []
if not os.path.isdir(folder_path + "\\" + searchTag):
    os.mkdir(folder_path + "\\" + searchTag)

count = 0
step = 4
# 크롬드라이버 연결 및 무신사 이동
driver = webdriver.Chrome('D:\\GraduationProject-Team3\\chromedriver_win32\\chromedriver.exe')

driver.get('https://www.musinsa.com/')
# 오류 방지를 위해 화면 최대화 적용
driver.maximize_window()
# 검색창에 검색어 입력
musinsaSearch_box = driver.find_element(By.XPATH, '//*[@id="search_query"]')
musinsaSearch_box.click()
musinsaSearch_box.send_keys(searchTag)
musinsaSearch_box.send_keys(Keys.RETURN)
# 무신사 상품 탭으로 이동
driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/section/nav/a[2]').click()
# 현재 페이지의 정보를 BeautifulSoup 라이브러리
pageString = driver.page_source
soup = BeautifulSoup(pageString, features='html.parser')
# 검색한 상품의 총 개수를 저장
Af = soup.find_all('a', attrs={'class': 'img-block'})[0]['data-bh-custom-total-count']
dateLeng = [datetime.today().year, datetime.today().month, datetime.today().day]
writer.writerow(dateLeng)
info = ['product_name', 'original_price', 'discounted_price', 'discount_rate', 'image_link', 'search_keyword', 'purchase_link']
writer.writerow(info)

# CREATE TABLE product_info (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     product_name VARCHAR(255) NOT NULL,
#     original_price INT NOT NULL,
#     discounted_price INT NOT NULL,
#     discount_rate INT NOT NULL,
#     image_link VARCHAR(500) NOT NULL,
#     search_keyword VARCHAR(255) NOT NULL,
#     purchase_link VARCHAR(500) NOT NULL
# );

while 1:

    time.sleep(2)

    i = 0
    b = 0
    length = soup.find_all('a', attrs={'class': 'img-block'})

    for a in length:
        b = b + 1
    while i < b:
        # 상품의 개수만큼 검색 후 CSV 파일에 입력
        title = soup.find_all('a', attrs={'class': 'img-block'})[i]['title']
        price = soup.find_all('a', attrs={'class': 'img-block'})[i]['data-bh-content-meta2']
        salePrice = soup.find_all('a', attrs={'class': 'img-block'})[i]['data-bh-content-meta3']
        salePercentage = soup.find_all('a', attrs={'class': 'img-block'})[i]['data-bh-content-meta5']
        link = soup.find_all('a', attrs={'class': 'img-block'})[i]['href']
        img = "http:" + soup.find_all('img', attrs={'class': 'lazyload lazy'})[i]['data-original']
        i = i + 1
        count = count + 1

        print(title)
        arrayItem.append(title)
        print(price)
        arrayItem.append(price)
        arrayItem.append(salePrice)
        arrayItem.append(salePercentage)
        arrayItem.append(img)
        arrayItem.append(searchTag)
        arrayItem.append(link)
        writer.writerow(arrayItem)
        arrayItem.clear()
        name = "\image" + str(count) + ".jpg"
        # 이미지 저장
        urllib.request.urlretrieve(img, folder_path + "\\" + searchTag + name)

    # 페이지 이동을 위한 CSS 설정
    leng = '#goodsList > div.sorter-box.box > div > div > a:nth-child(' + str(step) + ')'

    # 현재 검색한 상품 개수가 총 상품 개수와 같아졌을 시 종료
    if (count == int(Af)):
        time.sleep(2)
        break
    # 페이지 이동
    driver.find_element(By.CSS_SELECTOR, leng).click()
    step = step + 1
    if (step == 14):
        step = step - 10
    # 이동한 페이지를 검색페이지로 설정
    pageString = driver.page_source
    soup = BeautifulSoup(pageString, features='html.parser')