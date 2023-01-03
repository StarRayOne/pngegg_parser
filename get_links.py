import time
import csv
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import lxml

ua = UserAgent()
fake_head = {'user-agent': ua.random}

all_links = []


def get_all_pages():
    page = 1
    while True:
        response = requests.get(url=f'https://www.pngegg.com/en/search?q=png&page={page}', headers=fake_head)
        print(page, response.status_code)  # удалить
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, 'lxml')
        links = [link.find('a')['href'] for link in soup.find_all('figure')]
        all_links.extend(links)
        page += 1
    print(len(all_links))

def get_images_and_info():
    get_all_pages()
    print(len(all_links))
    count = 0
    with open('links.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(["link", "link_download"])

    for number in range(len(all_links)):
        try:
            fake_head = {'user-agent': ua.random}
            response = requests.get(url=all_links[number], headers=fake_head)
            soup = BeautifulSoup(response.text, 'lxml')
            links = []
            # иногда встречаются другие теги, сделать отработку добавить тут разрешение картинки по тз
            info = soup.find(class_="info_detail").text
            info = info[:-2].split('x')
            info = [int(i) for i in info]
            # print(info)
            # print(f'Ссылка {all_links[number]}, Номер страницы: {number}, Количество подходящих картинок: {count}')
            if info[0] >= 999 or info[1] >= 999:
                count += 1
                link = soup.find('a', class_="dld_btn bgcolor")['href']
                with open('links.csv', 'a', newline='\n') as file:
                    writer = csv.writer(file, delimiter=',')
                    writer.writerow([f"{all_links[number]}", f"{link}"])
        except:
            print('Что-то сломалось')
            pass
    print('Мы закончили!')
get_images_and_info()