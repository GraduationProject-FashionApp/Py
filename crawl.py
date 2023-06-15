from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.request
import time
import os
import csv
from selenium.webdriver.chrome.service import Service

folder_path = 'D:\\GraduationProject-Team3\\testImage'
csv_file_path = 'D:\\GitRepo\\Py\\dataCrawl.csv'
searchTag = input("Type searchTag: ")
arrayItem = []

if not os.path.isdir(folder_path + "\\" + searchTag):
    os.mkdir(folder_path + "\\" + searchTag)

count = 0
step = 4

# 크롬드라이버 연결 및 무신사 이동
# Create a service object
s = Service(r'D:\GraduationProject-Team3\chromedriver_win32_90\chromedriver.exe')

# Pass the service object to the driver
driver = webdriver.Chrome(service=s)

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
total_count = int(soup.find_all('a', attrs={'class': 'img-block'})[0]['data-bh-custom-total-count'])

# CSV 파일 생성 및 feature 정보 작성
file_exists = os.path.isfile(csv_file_path)
with open(csv_file_path, 'a', newline="", encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    if not file_exists:
        dateLeng = [datetime.today().year, datetime.today().month, datetime.today().day]
        writer.writerow(dateLeng)
        info = ['product_name', 'original_price', 'discounted_price', 'discount_rate', 'image_link', 'search_keyword', 'purchase_link']
        writer.writerow(info)

    max_items = 1000
    flag = 1

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
            name = "\\image" + str(count) + ".jpg"
            # 이미지 저장
            urllib.request.urlretrieve(img, folder_path + "\\" + searchTag + name)

        # 페이지 이동을 위한 CSS 설정
        leng = '#goodsList > div.sorter-box.box > div > div > a:nth-child(' + str(step) + ')'

        # 현재 검색한 상품 개수가 총 상품 개수와 같아졌을 시 혹은 1000개 이상 등록 시 종료
        if count == total_count or count > max_items:
            time.sleep(2)
            break
        # 페이지 이동
        driver.find_element(By.CSS_SELECTOR, leng).click()
        step = step + 1
        if step == 14:
            step = step - 10
        # 이동한 페이지를 검색페이지로 설정
        pageString = driver.page_source
        soup = BeautifulSoup(pageString, features='html.parser')
