import json

import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
from pprint import pprint

HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
KEYWORDS = ['Django', 'Flask']

def get_headers():
    return Headers(browser='firefox', os='win').generate()


SOURCE = requests.get(HOST, headers=get_headers()).text

bs = BeautifulSoup(SOURCE, features='lxml')

articles_list = bs.find_all(class_="vacancy-serp-item__layout")

vacancy_list = []

for article in articles_list:
    link = article.find('a')['href']
    salary = article.find('span', class_="bloko-header-section-3")
    company = article.find('a', class_='bloko-link bloko-link_kind-tertiary').text
    city = article.find('div',{'data-qa':'vacancy-serp__vacancy-address'}).text

    vacancy_list.append({

        'Зарплата': salary,
        'Компания': company,
        'Город': city,
        'Ссылка': link

    })

pprint(vacancy_list)

with open('vacancy.json', 'w') as f:
    json.dump(vacancy_list, f)