import requests
from bs4 import BeautifulSoup
import json
import csv

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
# receive all pages with products
url = 'https://terrasport.ua/football/view=smalltile/'

all_pages = [url]
for count in range(2, 20):
    basic_url = f'https://terrasport.ua/football/page={count}/view=smalltile/'
    all_pages.append(basic_url)

# prepare table with headers
with open(f'data/all_products.csv', mode='w', encoding='UTF-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(('id', 'page', 'name', 'image', 'price', 'status'))

all_info = {}
number_of_pages = 19
cur_page = 1
iteration_number = 1
for page in all_pages:
    print(f'Pages left to go: {number_of_pages - cur_page}')

    req = requests.get(page, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, 'lxml')
    products = soup.find('ul', class_='stores3').find_all(class_="icon")
    for a in products:
        print(f'number of product: {iteration_number}')
        # page with a specific product
        prd = a.get('href')

        req = requests.get(prd, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')

        # get information
        id = soup.find(class_="code").text.split(' ')[-1]
        page = cur_page
        try:
            name = soup.find('h1').text
        except Exception:
            name = 'empty h1'

        try:
            image = soup.find(class_='mainimage').find('img').get('src')
        except Exception:
            image = 'no photo'

        try:
            price = soup.find('div', class_='price').find('b').text + ' grn'
        except:
            price = 'not available'

        try:
            status = soup.find('div', class_='status').find('span').text
        except:
            status = 'no info'

        with open(f'data/all_products.csv', mode='a', encoding='UTF-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow((id, page, name, image, price, status))

        all_info[id] = {
            'page': page,
            'name': name,
            'image': image,
            'price': price,
            'status': status
        }

        iteration_number += 1
    cur_page += 1

with open('data/all_products_dict.json', 'w', encoding='UTF-8') as f:
    json.dump(all_info, f, indent=4, ensure_ascii=False)

print(f'successfully completed')
