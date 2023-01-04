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
    count = 0
    for link in range(len(all_links)):
        print(f'Скачали фоток {count}')

        try:
            response = requests.get(url=all_links[link], headers=fake_head)
            soup = BeautifulSoup(response.text, 'lxml')
            # игфо объекта
            resolution = soup.find(class_="info_detail").text
            name = soup.find(class_='view_h1 overflow').text
            count += 1
            tags = [i.text for i in soup.find(class_='tag_ul').find_all('li')]
            preview = soup.find('figure').find('img')['src']
            download_preview = requests.get(url=preview, stream=True)
            with open(f'preview/preview_image_{count}.png', 'wb') as prew:
                prew.write(download_preview.content)
            download_response = requests.get(url=all_download_links[link])
            download_soup = BeautifulSoup(download_response.text, 'lxml')
            print(count, f'pngimage_{count}', all_links[link], name, f'{[i for i in tags]}', resolution)
            with open('info.csv', 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow([count, f'pngimage_{count}', all_links[link], name, tags, resolution])
            flag = False
            while True:
                if flag == True:
                    break
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
                        # answer = solver.coordinates(img)
                        time.sleep(10)
                        while True:  # добавить иф если капчу сделали неправильно - пропускаем

                            browser.execute_script("window.scrollBy(0,-5)")
                            download_check = browser.find_element(By.ID, 'download_secs')
                            print(download_check.text)
                            if download_check.text == 'Your download will start shortly, please wait...':
                                flag = False
                                break
                            else:
                                flag = True
                                break
                            break

                else:
                    with webdriver.Chrome() as browser:
                        browser.get(all_download_links[link])
                        flag = True
                        time.sleep(5)

        except:
            pass

    print('Скачивание закончили!')
    print("--- %s секунд ---" % (time.time() - start_time))


get_images()
