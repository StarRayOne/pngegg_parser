import time
from twocaptcha import TwoCaptcha
import csv
from bs4 import BeautifulSoup
import requests
from threading import Thread
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

import lxml

all_links = []
all_download_links = []
ua = UserAgent()
fake_head = {'user-agent': ua.random}

config1 = {
    'server': 'rucaptcha.com',
    'apiKey': '1adfbaa28824f290e450fccf22125fac',
    'softId': 123,
    'callback': 'https://your.site/result-receiver',
    'defaultTimeout': 60,
    'recaptchaTimeout': 600,
    'pollingInterval': 10,
}
config2 = {
    'server': 'rucaptcha.com',
    'apiKey': 'dfc81ba1ac4fde79935f0759308a3b4f',
    'softId': 123,
    'callback': 'https://your.site/result-receiver',
    'defaultTimeout': 60,
    'recaptchaTimeout': 600,
    'pollingInterval': 10
}
proxy_twocaptcha={
    'type': 'HTTP',
    'uri': 'https://wbXVE2:7fzmTD@193.233.60.75:9545'
}
solver = TwoCaptcha(**config1)
solver2 = TwoCaptcha(**config2)


def get_images():
    with open('info.txt', 'w') as file:
        file.write('Старт отсюда!\n')
    with open('all_need_links.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            all_links.extend([row['link']])
            all_download_links.extend([row['link_download']])
    start_time = time.time()

    # парсер 1 (добавить процесс в отдельный тред)
    def parser1():
        count = 0
        for link in range(0, len(all_links), 2):
            with open('info.txt', 'a') as file:
                file.write(f'Парсер 1: {all_links[link]}, Кол-во ссылок: {count}\n')
            count += 1
            print(f'Парсер 1: {all_links[link]}, Кол-во ссылок: {count}')
            try:
                fake_head = {'user-agent': ua.random}
                response = requests.get(url=all_links[link], headers=fake_head)
                soup = BeautifulSoup(response.text, 'lxml')
                # собираем инфу с основной стр
                resolution = soup.find(class_="info_detail").text
                # чекаем страницу селениумом и скачиваем картинки
                download_response = requests.get(url=all_download_links[link])
                download_soup = BeautifulSoup(download_response.text, 'lxml')
                # если есть капча на странице
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
                        time.sleep(40)
                        captcha = requests.get(
                            url=f'http://rucaptcha.com/res.php?key=1adfbaa28824f290e450fccf22125fac&action=get&id={answer.get("captchaId", 0)}&json=1')

                        print(f"Парсер 1: {captcha.json()['request']}")
                        print(x1, y1, x2, y2, x3, y3, x4, y4)
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

                        # СЮДА ПЕРЕМЕСТИТЬ СКАЧИВАНИЕ ФАЙЛА И ЛОГ КАК ФАЙЛ СКАЧАЕТСЯ ПО ОБЩЕЙ ПЕРЕМЕННОЙ КАУНТ ИЛИ ПО ВРЕМЕНИ СКАЧИВАНИЯ ФАЙЛА (ДАТА СОЗДАНИЯ ФАЙЛА)
                else:
                    # если капчи нет
                    with webdriver.Chrome() as browser:
                        browser.get(all_download_links[link])
                        time.sleep(4)
                        # СЮДА ПЕРЕМЕСТИТЬ СКАЧИВАНИЕ ФАЙЛА И ЛОГ КАК ФАЙЛ СКАЧАЕТСЯ ПО ОБЩЕЙ ПЕРЕМЕННОЙ КАУНТ ИЛИ ПО ВРЕМЕНИ СКАЧИВАНИЯ ФАЙЛА
            except:
                pass

    # парсер 2 (с прокси) (добавить процесс в отдельный тред), не работаетпрокси в реквесте обычном
    # СКОРЕЕ ВСЕГО ПРОБЛЕМА В КУКАХ!!! ПОДМЕНИ КУКИ ИЛИ БРАУЗЕР НА ФАЕРФОКС
    # ПОВЕСИТЬ ЗАПИСЬ ИНФЫ В ФАЙЛ В КОНЦЕ ТОЛЬКО ЕСЛИ ФАЙЛ СКАЧАЛСЯ!!!!!
    # ДОБАВЛЯТЬ НАЗВАНИЕ ФАЙЛА ПО ССЫЛКЕ И УЗНАТЬ КАК ВЕСТИ ЛОГ СКАЧАННЫХ ФАЙЛОВ В СЕЛЕНИУМ https://ru.selenide.org/2016/08/27/selenide-3.9.1/https://ru.selenide.org/2016/08/27/selenide-3.9.1/
    # ИЛИ РЕКВЕСТ И ПРОВЕРКУ ПО ССЫЛКАМ ПЕРЕКИНУТЬ ВНИЗ ФУНКЦИИ (ПОСЛЕ СКАЧИВАНИЯ) И СКАЧИВАЕМ В СЛУЧАЕ  ЕСЛИ ОКНО УСПЕШНО ЗАКРЫЛОСЬ И ФАЙЛ СКАЧАЛСЯ
    # ТОЧНОЕ ВРЕМЯ СКАЧИВАНИЯ ФАЙЛА БУДЕТ ЕСЛИ ЗАПИСАТЬ ЕГО СРАЗУ ПОСЛЕ ЗАКРЫТИЯ ОКНА В ПЕРЕМЕННУЮ И УЖЕ ПОТОМ ЗАПИСЫВАТЬ В ФАЙЛИК
    def parser2():
        count = 0
        for link in range(1, len(all_links), 2):
            with open('info.txt', 'a') as file:
                file.write(f'Парсер 2: {all_links[link]}, Кол-во ссылок: {count}\n')
            count += 1
            proxy_request = {'http': "https://wbXVE2:7fzmTD@193.233.60.75:9545"}
            print(f'Парсер 2: {all_links[link]} Кол-во ссылок: {count}')
            try:
                fake_head = {'user-agent': ua.random}
                response = requests.get(url=all_links[link], headers=fake_head, proxies=proxy_request)
                soup = BeautifulSoup(response.text, 'lxml')
                # собираем инфу с основной стр
                resolution = soup.find(class_="info_detail").text
                # чекаем страницу селениумом и скачиваем картинки
                download_response = requests.get(url=all_download_links[link], proxies=proxy_request)
                download_soup = BeautifulSoup(download_response.text, 'lxml')
                # если есть капча на странице
                proxy = {'proxy': {
                    'https': "https://wbXVE2:7fzmTD@193.233.60.75:9545",
                }}
                if 'I am human ' in download_soup.text:
                    with webdriver.Chrome(seleniumwire_options=proxy) as browser:
                        browser.get(all_download_links[link])
                        time.sleep(5)
                        i_human = browser.find_element(By.ID, 'imhuman')
                        browser.execute_script("return arguments[0].scrollIntoView(true);", i_human)
                        browser.execute_script("window.scrollBy(0,-150)")
                        browser.find_element(By.ID, 'imhuman').click()
                        time.sleep(2)
                        img = browser.find_element(By.ID, 'pcaptcha').find_element(By.TAG_NAME, 'img')
                        img = img.get_attribute('src')
                        answer = solver2.coordinates(img, **proxy_twocaptcha)
                        time.sleep(40)
                        captcha = requests.get(
                            url=f'http://rucaptcha.com/res.php?key=dfc81ba1ac4fde79935f0759308a3b4f&action=get&id={answer.get("captchaId", 0)}&json=1')
                        print(f"Парсер 2: {captcha.json()['request']}")

                        x1 = captcha.json()['request'][0].get('x', 0)
                        y1 = captcha.json()['request'][0].get('y', 0)
                        x2 = captcha.json()['request'][1].get('x', 0)
                        y2 = captcha.json()['request'][1].get('y', 0)
                        x3 = captcha.json()['request'][2].get('x', 0)
                        y3 = captcha.json()['request'][2].get('y', 0)
                        x4 = captcha.json()['request'][3].get('x', 0)
                        y4 = captcha.json()['request'][3].get('y', 0)
                        print(x1, y1, x2, y2, x3, y3, x4, y4)
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
                        # СЮДА ПЕРЕМЕСТИТЬ СКАЧИВАНИЕ ФАЙЛА И ЛОГ КАК ФАЙЛ СКАЧАЕТСЯ ПО ОБЩЕЙ ПЕРЕМЕННОЙ КАУНТ ИЛИ ПО ВРЕМЕНИ СКАЧИВАНИЯ ФАЙЛА
                else:
                    # если капчи нет
                    with webdriver.Chrome(seleniumwire_options=proxy) as browser:
                        browser.get(all_download_links[link])
                        time.sleep(4)
                        # СЮДА ПЕРЕМЕСТИТЬ СКАЧИВАНИЕ ФАЙЛА И ЛОГ КАК ФАЙЛ СКАЧАЕТСЯ ПО ОБЩЕЙ ПЕРЕМЕННОЙ КАУНТ ИЛИ ПО ВРЕМЕНИ СКАЧИВАНИЯ ФАЙЛА
            except:
                pass

    # Thread(target=parser1).start()
    Thread(target=parser2).start()


get_images()
