from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd


options = webdriver.ChromeOptions()
# options.add_argument('--disable-blink-features=AutomationControlled') # Убираем сигнатуру Selenium
# options.add_argument('--headless')  # Запуск в фоновом режиме
# options.add_argument('--disable-gpu')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
driver = webdriver.Chrome(options=options)

baseurl = 'https://quotes.toscrape.com/'

def wait_for_data(css_selector, timeout=15):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        print("Data appeared!")
    except Exception as e:
        print("Timeout: Data did not appear within the given time.")

def parse_quote(el):
    text = el.find('span', class_='text').text
    author = el.find('small', class_='author').text
    tags = el.find_all('a', class_='tag')
    all_tags_text = [tag.text for tag in tags]

    quote = {
        'text': text,
        'author': author,
        'tags': all_tags_text
    }

    # print("Text:", text)
    # print("Author:", author)
    # print("Tags:", all_tags_text)

    return quote


if __name__ == '__main__':

    quotes_list = []
    for i in range(1, 11):
        driver.get(f'https://quotes.toscrape.com/js-delayed/page/{i}/')
        wait_for_data('.quote')

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        all_quotes = soup.find_all('div', class_='quote')
        print(f"Page {i}: {len(all_quotes)}")
        for quote_tag in all_quotes:
            quote = parse_quote(quote_tag)
            quotes_list.append(quote)

    driver.quit()

    df = pd.DataFrame(quotes_list)
    df.to_excel('quotes.xlsx', index=False)