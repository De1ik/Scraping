from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

from concurrent.futures import ThreadPoolExecutor


options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled') # Убираем сигнатуру Selenium
options.add_argument('--headless')  # Запуск в фоновом режиме
options.add_argument('--disable-gpu')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')



baseurl = 'https://www.thewhiskyexchange.com'
page_url = 'https://www.thewhiskyexchange.com/search/all/scotch-whisky?pg=2'
total_items = 186



# collect all pages (links) with data
product_links = []

for i in range(1, 3):
    driver = webdriver.Chrome(options=options)
    page_url = f'https://www.thewhiskyexchange.com/search/all/scotch-whisky?pg={i}'
    print(f'Page {i}: {page_url}')
    driver.get(page_url)
    html_data = driver.page_source

    # with open('data/page.html', 'w', encoding='utf-8') as file:
    #     file.write(html)


    # with open('data/page.html', 'r', encoding='utf-8') as file:
    #     html_data = file.read()

    soup = BeautifulSoup(html_data, 'html.parser')

    product_items = soup.find_all('li', class_='product-grid__item')

    for item in product_items:
        link = item.find('a', href=True)
        # print(baseurl + link.get('href'))
        product_links.append(baseurl + link.get('href'))

        with open('data/product-links.txt', 'a+') as f:
            f.write(baseurl + link.get('href') + '\n')

    driver.quit()


print("Amount of product items:", len(product_links))



with open('data/product-links.txt', 'r') as f:
    for line in f:
        product_links.append(line.strip())


# collect data from the specific page

def scrape_product(args):
    i, link = args
    driver = webdriver.Chrome(options=options)
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    item_data = {}

    try:
        name_tag = soup.find('h1', class_='product-main__name')
        name = name_tag.contents[0].strip()
    except:
        name = 'Error'

    try:
        price = soup.find('p', class_='product-action__price').get_text()
    except:
        price = 'Error'

    item_data['name'] = name.strip()
    item_data['price'] = price.strip()

    try:
        all_facts = soup.find_all('li', class_='product-facts__item')
    except:
        all_facts = []

    for fact in all_facts:
        try:
            key = fact.find('h3', class_='product-facts__type').get_text()
            value = fact.find('p', class_='product-facts__data').get_text()
        except:
            key = 'Error'
            value = 'Error'
        item_data[key.strip()] = value.strip()

    driver.quit()
    print(f"{i} Saved: {name}, {link}")
    return item_data


with ThreadPoolExecutor() as executor:
    data_for_df = list(executor.map(scrape_product, enumerate(product_links)))

print("ok")
# Create df and save data to excel sheet
df = pd.DataFrame(data_for_df)
df.to_excel('data/whisky_data.xlsx', sheet_name='Whisky Info', index=False)
print("Data saved to whisky_data.xlsx")
