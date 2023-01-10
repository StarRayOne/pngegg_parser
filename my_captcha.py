import time
from twocaptcha import TwoCaptcha
import csv
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
import os

import lxml

all_links = []
all_download_links = []
fake_head = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

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
    with open('info_all.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if row['image_name'] == 'del':
                all_links.extend([row['link']])
    print(len(all_links))
    start_time = time.time()
    count = 1
    for link in range(len(all_links)):
        print(f'Скачиваем фото {count} - {all_links[link]}')
        response = requests.get(url=all_links[link], headers=fake_head)
        soup = BeautifulSoup(response.text, 'lxml')
        # игфо объекта

        preview = soup.find('figure').find('img')['src']
        download_preview = requests.get(url=preview, stream=True)
        with open(f'preview/preview_image_{count}.png', 'wb') as prew:
            prew.write(download_preview.content)
        count += 1

    print('Скачивание закончили!')
    print("--- %s секунд ---" % (time.time() - start_time))


get_images()
