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
    with open('all_need_links.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            all_links.extend([row['link']])
            all_download_links.extend([row['link_download']])
    with open('info.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["number", 'image_name', 'link', 'name', 'tags', 'resolution'])
    print(len(all_links))
    start_time = time.time()
    count = 2687
    for link in range(2686, len(all_links)):
        print(f'Скачиваем фото {count} - {all_links[link]}')
        try:
            response = requests.get(url=all_links[link], headers=fake_head)
            soup = BeautifulSoup(response.text, 'lxml')
            # игфо объекта
            resolution = soup.find(class_="info_detail").text
            name = soup.find(class_='view_h1 overflow').text
            tags = [i.text for i in soup.find(class_='tag_ul').find_all('li')]
            preview = soup.find('figure').find('img')['src']
            download_preview = requests.get(url=preview, stream=True)
            with open(f'preview/preview_image_{count}.png', 'wb') as prew:
                prew.write(download_preview.content)
            with open('info.csv', 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow([count, f'pngimage_{count}', all_links[link], name, tags, resolution])
            # настройки цикла проверки капчи
            flag = True
            directory1 = '/home/hack/Загрузки/'
            directory2 = '/home/hack/PycharmProjects/1. Заказы фриланс в работе/png_parser/preview/'
            while True:
                preview = [file for file in os.listdir(directory2) if
                           os.path.isfile(f'{directory2}/{file}')]
                if flag == False:
                    break
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
                        while True:  # добавить иф если капчу сделали неправильно - пропускаем
                            captcha = requests.get(
                                url=f'http://rucaptcha.com/res.php?key=1adfbaa28824f290e450fccf22125fac&action=get&id={answer.get("captchaId", 0)}&json=1')
                            if captcha.json()['request'] == 'CAPCHA_NOT_READY':
                                print(f'Капча #{count} не готова!')
                                time.sleep(5)
                            else:
                                print(f"Капча готова!")
                                x1 = captcha.json()['request'][0].get('x', 0)
                                y1 = captcha.json()['request'][0].get('y', 0)
                                x2 = captcha.json()['request'][1].get('x', 0)
                                y2 = captcha.json()['request'][1].get('y', 0)
                                x3 = captcha.json()['request'][2].get('x', 0)
                                y3 = captcha.json()['request'][2].get('y', 0)
                                x4 = captcha.json()['request'][3].get('x', 0)
                                y4 = captcha.json()['request'][3].get('y', 0)

                                captcha = browser.find_element(By.ID, 'pcaptcha-container').find_element(By.TAG_NAME,
                                                                                                         'img')
                                ActionChains(browser).move_to_element_with_offset(captcha, -135, -175).move_by_offset(
                                    x1,
                                    y1).click().perform()
                                ActionChains(browser).move_to_element_with_offset(captcha, -135, -175).move_by_offset(
                                    x2,
                                    y2).click().perform()
                                ActionChains(browser).move_to_element_with_offset(captcha, -135, -175).move_by_offset(
                                    x3,
                                    y3).click().perform()
                                ActionChains(browser).move_to_element_with_offset(captcha, -135, -175).move_by_offset(
                                    x4,
                                    y4).click().perform()
                                time.sleep(10)

                                images = [file for file in os.listdir(directory1) if
                                          os.path.isfile(f'{directory1}/{file}')]
                                try:
                                    if browser.find_element(By.ID,
                                                            'download_secs').text == 'Your download will start shortly, please wait...':
                                        print('Не та капча!')
                                        flag = True
                                        break
                                except:
                                    pass
                                if len(images) == len(preview):
                                    flag = False
                                    break
                                else:
                                    print('Не успеваю скачать фото после ввода капчи... Жду ещё 30 секунд!')
                                    time.sleep(30)
                                    images = [file for file in os.listdir(directory1) if
                                              os.path.isfile(f'{directory1}/{file}')]
                                    flag = False
                                    if len(images) != len(preview):
                                        print('Через 30 секунд после ввода капчи ничего не скачало! Жду еще 30')
                                        time.sleep(30)
                                        images = [file for file in os.listdir(directory1) if
                                                  os.path.isfile(f'{directory1}/{file}')]
                                        flag = False
                                        if len(images) != len(preview):
                                            print('Через 80 секунд после ввода капчи ничего не скачало! Пробую ещё раз')
                                            flag = True

                else:
                    with webdriver.Chrome() as browser:
                        browser.get(all_download_links[link])
                        time.sleep(10)
                        images = [file for file in os.listdir(directory1) if
                                  os.path.isfile(f'{directory1}/{file}')]
                        flag = False
                        if len(images) == len(preview):
                            break
                        else:
                            print('Не успеваю скачать фото без капчи... Жду ещё 30 секунд!')
                            time.sleep(30)
                            images = [file for file in os.listdir(directory1) if
                                      os.path.isfile(f'{directory1}/{file}')]
                            flag = False
                            if len(images) != len(preview):
                                print('Не получилось скачать фото без капчи после 30 сек ожидания, жду ещё 30 сек!')
                                time.sleep(30)
                                images = [file for file in os.listdir(directory1) if
                                          os.path.isfile(f'{directory1}/{file}')]
                                flag = False
                                if len(images) != len(preview):
                                    print('Не могу скачать фото без капчи после 60 сек ожидания... пробую ещё раз!')
                                    flag = True



        except:
            pass
        count += 1

    print('Скачивание закончили!')
    print("--- %s секунд ---" % (time.time() - start_time))


get_images()
