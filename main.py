import time
import twocaptcha
from twocaptcha import TwoCaptcha
import csv
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import lxml
all_links = []
all_download_links = []
ua = UserAgent()
fake_head = {'user-agent': ua.random}

config = {
            'server':           'rucaptcha.com',
            'apiKey':           '1adfbaa28824f290e450fccf22125fac',
            'softId':            123,
            'callback':         'https://your.site/result-receiver',
            'defaultTimeout':    60,
            'recaptchaTimeout':  600,
            'pollingInterval':   10,
        }

solver = TwoCaptcha(**config)


def get_images():
    with open('all_need_links.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            all_links.extend([row['link']])
            all_download_links.extend([row['link_download']])
    print(len(all_links))
    print(len(all_download_links))
    for link in range(len(all_links)):

        fake_head = {'user-agent': ua.random}
        response = requests.get(url=all_links[link], headers=fake_head)
        soup = BeautifulSoup(response.text, 'lxml')
        resolution = soup.find(class_="info_detail").text
        # info = info[:-2].split('x') нужны были только для проверки
        # info = [int(i) for i in info]
        # селениум нужно интегрировать с анти капчей и заносить картинки в зип
        # link_down = soup.find('a', class_="dld_btn bgcolor")['href'] # доделать селениум
        with webdriver.Chrome() as browser:
            browser.get(all_download_links[link])
            browser.execute_script("window.scrollBy(0,610)")
            browser.find_element(By.ID, 'imhuman').click()
            time.sleep(4)
            img = browser.find_element(By.ID, 'pcaptcha').find_element(By.TAG_NAME, 'img')
            img = img.get_attribute('src')
            answer = solver.coordinates(img)
            print(img)
            time.sleep(60)
            captcha = requests.get(
                url=f'http://rucaptcha.com/res.php?key=1adfbaa28824f290e450fccf22125fac&action=get&id={answer.get("captchaId", 0)}&json=1')

            print(captcha.json()['request'])
            x1 = captcha.json()['request'][0].get('x', 0)
            y1 = captcha.json()['request'][0].get('y', 0)
            x2 = captcha.json()['request'][1].get('x', 0)
            y2 = captcha.json()['request'][1].get('y', 0)
            x3 = captcha.json()['request'][2].get('x', 0)
            y3 = captcha.json()['request'][2].get('y', 0)
            x4 = captcha.json()['request'][3].get('x', 0)
            y4 = captcha.json()['request'][3].get('y', 0)

            captcha = browser.find_element(By.ID, 'pcaptcha-container').find_element(By.TAG_NAME, 'img')
            ActionChains(browser).move_to_element_with_offset(captcha,-130, -165).move_by_offset(x1, y1).click().perform()
            ActionChains(browser).move_to_element_with_offset(captcha,-130, -165).move_by_offset(x2, y2).click().perform()
            ActionChains(browser).move_to_element_with_offset(captcha,-130, -165).move_by_offset(x3, y3).click().perform()
            ActionChains(browser).move_to_element_with_offset(captcha,-130, -165).move_by_offset(x4, y4).click().perform()
            time.sleep(15)


    print()


get_images()

# 1.82845  баланс