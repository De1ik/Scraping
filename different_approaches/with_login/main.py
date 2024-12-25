from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import time


options = webdriver.ChromeOptions()
# options.add_argument('--disable-blink-features=AutomationControlled') # Убираем сигнатуру Selenium
# options.add_argument('--headless')  # Запуск в фоновом режиме
# options.add_argument('--disable-gpu')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
driver = webdriver.Chrome(options=options)

baseurl = 'https://quotes.toscrape.com/'



def parse_quote(el):
    text = el.find('span', class_='text').text
    author = el.find('small', class_='author').text
    author_link = el.find('a', href=True)
    tags = el.find_all('a', class_='tag')
    all_tags_text = [tag.text for tag in tags]

    quote = {
        'text': text,
        'author': author,
        'author_link': baseurl + author_link.get('href'),
        'tags': all_tags_text
    }

    # print("Text:", text)
    # print("Author:", author)
    # print("Tags:", all_tags_text)

    return quote


def login():
    driver.get('https://quotes.toscrape.com/login')

    username_field = driver.find_element(By.NAME, "username")
    username_field.send_keys("username")

    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys("password")

    login_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
    login_button.click()

    time.sleep(2)


def go_next_page(css_selector, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        next_page_button = driver.find_element(By.CSS_SELECTOR, css_selector)
        next_page_button.click()
        print("[*] Next page exists")
        return True
    except Exception as e:
        print("[!] No more pages")
        return False


if __name__ == '__main__':

    login()
    quotes_list = []

    isNextPage = True
    counter = 0
    while isNextPage:
        counter+=1
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        all_quotes = soup.find_all('div', class_='quote')
        print(f"Page {counter}: {len(all_quotes)}")
        for quote_tag in all_quotes:
            quote = parse_quote(quote_tag)
            quotes_list.append(quote)

        isNextPage = go_next_page("li.next > a")

    driver.quit()

    df = pd.DataFrame(quotes_list)
    df.to_excel('quotes.xlsx', index=False)