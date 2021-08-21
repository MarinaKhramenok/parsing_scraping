'''
1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
 сохранить JSON-вывод в файле *.json.
'''
import requests
import json

# https://api.github.com/users/MarinaKhramenok/repos
my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
# user = input('Введите username: ')
user = 'MarinaKhramenok'
response = requests.get('http://api.github.com/users/' + user + '/repos', headers=my_headers)
data_file = response.json()

with open('data.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_file,json_file)
