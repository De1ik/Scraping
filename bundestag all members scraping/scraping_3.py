import random

from bs4 import BeautifulSoup
import requests
import csv
import json
from time import sleep

# make the first row for csv table
with open('data/members_information.csv', 'w', encoding='UTF-8') as f:
    writer = csv.writer(f)
    writer.writerow(
        (
            'person_name',
            'person_company',
            'social_networks',
            'person_photo'
        )
    )

# main link
url = 'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=9999&view=BTBiographyList'
headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

# page with all members
req = requests.get(url, headers=headers)
src = req.text

with open('all_links.html', 'w', encoding='utf-8') as f:
    f.write(src)

with open('all_links.html', 'r', encoding='utf-8') as f:
    src = f.read()

soup = BeautifulSoup(src, 'lxml')

#  get the personal link for each member
all_links = soup.find_all('a')
with open('all_members_links.txt', 'w', encoding='utf-8') as f:
    for i in all_links:
        f.write(i.get('href') + '\n')

with open('all_members_links.txt', 'r', encoding='utf-8') as f:
    links = f.readlines()
    data_dict = []

count = 0

# get link with member information
for link in links:
    req = requests.get(link.strip(), headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    count += 1

    # get personal information
    try:
        person_name, person_company = soup.find('h3').text.strip().split(', ')
    except Exception:
        person_name = person_company = 'no info'

    try:
        person_photo = 'https://www.bundestag.de' + soup.find(class_='bt-bild-standard pull-left').find('img').get(
            'data-img-md-normal')
    except Exception:
        person_photo = 'no photo'

    try:
        social_networks = []
        all_networks = soup.find(class_='bt-linkliste').find_all('a')
        for link in all_networks:
            social_networks.append(link.get('href'))
    except Exception:
        social_networks = 'no info'

    data = {
        'person_photo': person_photo,
        'person_name': person_name,
        'person_company': person_company,
        'social_networks': social_networks,
    }

    with open('data/members_information.csv', 'a', encoding='UTF-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(
            (
                person_name,
                person_company,
                person_photo,
                social_networks,
            )
        )
        data_dict.append(data)

        print(f'personal data №{count} has been collected')

    with open('data/members_information.json', 'w', encoding='UTF-8') as f:
        json.dump(data_dict, f, indent=4, ensure_ascii=False)

    sleep(random.randrange(2, 4))

print('Scraping completed seccesfully')
