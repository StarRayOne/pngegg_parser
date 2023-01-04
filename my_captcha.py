import time
from twocaptcha import TwoCaptcha
import csv
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

import lxml

all_links = []
all_download_links = []
fake_head = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

config = {
    'server': 'rucaptcha.com',
    'apiKey': '1adfbaa28824f290e450fccf22125fac',
    'softId': 123,
    'callback': 'https://your.site/result-receiver',
    'defaultTimeout': 60,
    'recaptchaTimeout': 600,
    'pollingInterval': 10,
}

solver = TwoCaptcha(**config)


def get_images():
    with open('all_need_links.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            all_links.extend([row['link']])
            all_download_links.extend([row['link_download']])
    print(len(all_links))
    count = 0
    start_time = time.time()
    for link in range(len(all_links)):
        count += 1
        try:
            response = requests.get(url=all_links[link], headers=fake_head)
            soup = BeautifulSoup(response.text, 'lxml')
            resolution = soup.find(class_="info_detail").text
            # селениум нужно интегрировать с анти капчей и заносить картинки в зип
            # link_down = soup.find('a', class_="dld_btn bgcolor")['href'] # доделать селениум

            download_response = requests.get(url=all_download_links[link])
            download_soup = BeautifulSoup(download_response.text, 'lxml')
            if 'I am human ' in download_soup.text:
                with webdriver.Chrome() as browser:
                    browser.get(all_download_links[link])
                    i_human = browser.find_element(By.ID, 'imhuman')
                    browser.execute_script("return arguments[0].scrollIntoView(true);", i_human)
                    browser.execute_script("window.scrollBy(0,-150)")
                    browser.find_element(By.ID, 'imhuman').click()
                    time.sleep(10)

            else:
                with webdriver.Chrome() as browser:
                    browser.get(all_download_links[link])
                    time.sleep(3)
            if count == 100:
                break
        except:
            pass
    print('Скачивание закончили!')
    print("--- %s секунд ---" % (time.time() - start_time))

get_images()

