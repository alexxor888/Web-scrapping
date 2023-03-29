import json

import requests
import lxml
from fake_headers import Headers
from bs4 import BeautifulSoup
from pprint import pprint

HOST = 'https://spb.hh.ru/search/vacancy?text=python,django,flask&area=1&area=2'


def get_headers():
    return Headers(browser='firefox', os='win').generate()


SOURCE = requests.get(HOST, headers=get_headers()).text

bs = BeautifulSoup(SOURCE, features='lxml')

articles_list = bs.find_all(class_="vacancy-serp-item__layout")


vacancy_list = []
for article in articles_list:
    link = article.find('a')['href']
    salary = str(article.find('span', class_="bloko-header-section-3"))
    salary = salary.replace('<span class="bloko-header-section-3" data-qa="vacancy-serp__vacancy-compensation">','')\
        .replace('\u202f000','').replace('<!-- -->','тыс. ').replace('.</span>','.')
    company = article.find('a', class_='bloko-link bloko-link_kind-tertiary').text
    company = company.replace('\xa0', ' ')
    city = article.find('div',{'data-qa':'vacancy-serp__vacancy-address'}).text

    vacancy_list.append({

        'Компания': company,
        'Город': city,
        'Зарплата': salary,
        'Ссылка': link

    })

# pprint(vacancy_list)

with open('vacancy.json', 'w') as file:
    json.dump(vacancy_list, file, ensure_ascii=False)


# with open('vacancy.json') as f:
#     data = f.read()
#     data_json = json.loads(data)
#
# pprint(data_json)