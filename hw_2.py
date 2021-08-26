from pprint import pprint
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np


url = 'https://hh.ru'
hh_vacancy = pd.DataFrame(columns=['name', 'link', 'salary'])


for i in range(40):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
    params = {'fromSearchLine': 'true',
              'st': 'searchVacancy',
              'text': 'python',
              'page': i
              }
    response = requests.get(url + '/search/vacancy', headers=headers, params=params)
    soup = bs(response.text, 'html.parser')
    vacancys = soup.find_all('div', {'class': 'vacancy-serp-item'})

    vacancy_list = []
    for vacancy in vacancys:
        vacancy_data = {}
        link = vacancy.find('a')
        vacancy_link = link.get('href')
        vacancy_name = link.getText()

        try:
            vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        except:
            vacancy_salary = np.NaN

        if vacancy_salary:
            salary_text = vacancy_salary.text.replace('\u202f', '')
            vacancy_salary = salary_text.split(' ')

        vacancy_data['name'] = vacancy_name
        vacancy_data['link'] = vacancy_link
        vacancy_data['salary'] = vacancy_salary
        vacancy_list.append(vacancy_data)

    pprint(vacancy_list)

    hh_vacancy = pd.DataFrame(vacancy_list)
    hh_vacancy.to_csv('hh_vacancy.csv', index=False, encoding='utf-8')