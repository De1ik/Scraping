from bs4 import BeautifulSoup
import json
import requests
import csv
from collections import defaultdict

url = 'https://calorizator.ru/product'
headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

req = requests.get(url, headers=headers)
src = req.text

# save the main page for future work
with open('index.html', 'w', encoding='UTF-8') as file:
    file.write(src)

with open('index.html', 'r', encoding='UTF-8') as f:
    src = f.read()

soup = BeautifulSoup(src, 'lxml')

all_categories_dict = defaultdict(list)
iterations_count = 0
products = soup.find_all(class_="product")
for prd in products:
    all_links = prd.find_all('a')
    for page in all_links:
        name = page.text

        rep = [' ', ',', '-']
        for item in rep:
            if item in name:
                name = name.replace(item, '_')

        link = 'https://calorizator.ru/' + page.get('href')
        all_categories_dict[name] += [link]
        iterations_count += 1

        req = requests.get(link, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        not_check = [
            'Подбор продуктов',
            'Полный список продуктов',
            'Производители продуктов',
            'Личный кабинет',
            'Продукты в картинках']

        if soup.find('h1').text in not_check:
            continue

        try:
            all_links = soup.find(class_='item-list').find(class_='pager').find_all(class_='pager-item')
            for item in all_links:
                link = item.find('a')
                print('pages are being read')
                all_categories_dict[name] += ['https://calorizator.ru/' + link.get('href')]
                iterations_count += 1
        except:
            print('bad information')

with open('all_categories_dict.json', 'w', encoding='UTF-8') as f:
    json.dump(all_categories_dict, f, indent=4, ensure_ascii=False)

with open('all_categories_dict.json', 'r', encoding='UTF-8') as f:
    all_categories = json.load(f)


counter = 0
print(f'Total iterations: {iterations_count}')
for categories_name in all_categories:
    for categories_link in all_categories[categories_name]:
        req = requests.get(categories_link, headers=headers)
        src = req.text

        with open(f'data/{categories_name}.html', 'w', encoding='UTF-8') as f:
            f.write(src)

        with open(f'data/{categories_name}.html', 'r', encoding='UTF-8') as f:
            src = f.read()

        soup = BeautifulSoup(src, 'lxml')

        try:
            main_page = soup.find(class_='pager-current first')
            one_page = soup.find(class_='pager')
            if main_page is not None or one_page is None:
                products_thead = soup.find('thead').find_all('th')
                for item in products_thead[0]:
                    product = products_thead[1].text.strip()
                    squirrels = products_thead[2].text.strip()
                    fat = products_thead[3].text.strip()
                    crbhdr = products_thead[4].text.strip()
                    calories = products_thead[5].text.strip()

                    with open(f'data/{categories_name}.csv', mode='a', encoding='UTF-8', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(
                            (product,
                             squirrels,
                             fat,
                             crbhdr,
                             calories)
                        )
        except:
            iterations_count -= 1
            if iterations_count == 0:
                print(f'successfully completed')
                break
            print(f'{iterations_count} iterations left')
            continue

        products_data = soup.find('tbody').find_all('tr')

        for item in products_data:
            product_td = item.find_all('td')

            product = product_td[1].text.strip()
            squirrels = product_td[2].text.strip()
            fat = product_td[3].text.strip()
            crbhdr = product_td[4].text.strip()
            calories = product_td[5].text.strip()

            with open(f'data/{categories_name}.csv', mode='a', encoding='UTF-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        product,
                        squirrels,
                        fat,
                        crbhdr,
                        calories
                    )
                )

        iterations_count -= 1
        if iterations_count == 0:
            print(f'successfully completed')
        print(f'{iterations_count} iterations left')
        counter += 1