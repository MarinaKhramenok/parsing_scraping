from pprint import pprint
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from pymongo import MongoClient


url = 'https://hh.ru'
hh_vacancy = pd.DataFrame(columns=['name', 'link', 'salary', 'min_salary', 'max_salary', 'currency'])

client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']
hh_vacancies = db.hh_vacancies


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
    vacancies = soup.find_all('div', {'class': 'vacancy-serp-item'})

    vacancy_list = []
    for vacancy in vacancies:
        vacancy_data = {}
        link = vacancy.find('a')
        vacancy_link = link.get('href')
        vacancy_name = link.getText()


        vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})

        if vacancy_salary:
            min_salary = None
            max_salary = None
            salary_text = vacancy_salary.text.replace('\u202f', '')
            vacancy_salary = salary_text.split(' ')
            currency = salary_text.split()[-1]

            lst = [int(item) for item in vacancy_salary if item.isnumeric()]

            if '–' in vacancy_salary:
                min_salary = lst[0]
                max_salary = lst[1]
            elif 'от' in vacancy_salary:
                min_salary = lst[0]
                max_salary = None
            elif 'до' in vacancy_salary:
                min_salary = None
                max_salary = lst[0]

            salary_list = [min_salary, max_salary]
        else:
            vacancy_salary = np.NaN
            min_salary = np.NaN
            max_salary = np.NaN
            currency = np.NaN

        vacancy_data['name'] = vacancy_name
        vacancy_data['link'] = vacancy_link
        vacancy_data['salary'] = vacancy_salary
        vacancy_data['min_salary'] = min_salary
        vacancy_data['max_salary'] = max_salary
        vacancy_data['currency'] = currency
        vacancy_list.append(vacancy_data)

        
        hh_vacancies.update_one({'link': vacancy_data['link']}, {'$set': vacancy_data}, upsert=True)

    pprint(vacancy_list)

    hh_vacancy = pd.DataFrame(vacancy_list)
    hh_vacancy.to_csv('hh_vacancy.csv', index=False, encoding='utf-8')


def salary_get(num):
    i = 0
    for item in hh_vacancies.find({'$or': [{'min_salary': {'$gt': num}}, {'max_salary': {'$gt': num}}]}):
        pprint(item)
        i += 1
    print(f'{i} vacancies')

salary_get(10000)