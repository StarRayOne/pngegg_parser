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
    'apiKey': 'dfc81ba1ac4fde79935f0759308a3b4f',
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
    start_time = time.time()
    for link in range(len(all_links)):
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
                    time.sleep(2)
                    img = browser.find_element(By.ID, 'pcaptcha').find_element(By.TAG_NAME, 'img')
                    img = img.get_attribute('src')
                    answer = solver.coordinates(img)
                    time.sleep(10)
                    while True:
                        captcha = requests.get(
                            url=f'http://rucaptcha.com/res.php?key=dfc81ba1ac4fde79935f0759308a3b4f&action=get&id={answer.get("captchaId", 0)}&json=1')
                        if captcha.json()['request'] == 'CAPCHA_NOT_READY':
                            print('Капча не готова')
                            time.sleep(10)
                        else:
                            print(f"Парсер 1: {captcha.json()['request']}")
                            x1 = captcha.json()['request'][0].get('x', 0)
                            y1 = captcha.json()['request'][0].get('y', 0)
                            x2 = captcha.json()['request'][1].get('x', 0)
                            y2 = captcha.json()['request'][1].get('y', 0)
                            x3 = captcha.json()['request'][2].get('x', 0)
                            y3 = captcha.json()['request'][2].get('y', 0)
                            x4 = captcha.json()['request'][3].get('x', 0)
                            y4 = captcha.json()['request'][3].get('y', 0)

                            captcha = browser.find_element(By.ID, 'pcaptcha-container').find_element(By.TAG_NAME, 'img')
                            ActionChains(browser).move_to_element_with_offset(captcha, -135, -175).move_by_offset(x1,
                                                                                                                  y1).click().perform()
                            ActionChains(browser).move_to_element_with_offset(captcha, -135, -175).move_by_offset(x2,
                                                                                                                  y2).click().perform()
                            ActionChains(browser).move_to_element_with_offset(captcha, -135, -175).move_by_offset(x3,
                                                                                                                  y3).click().perform()
                            ActionChains(browser).move_to_element_with_offset(captcha, -135, -175).move_by_offset(x4,
                                                                                                                  y4).click().perform()
                            time.sleep(4)
                            break

                    else:
                        with webdriver.Chrome() as browser:
                            browser.get(all_download_links[link])
                            time.sleep(4)
        except:
            pass
    print('Скачивание закончили!')
    print("--- %s секунд ---" % (time.time() - start_time))

get_images()

