from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import pandas as pd
import time


options = webdriver.ChromeOptions()
# options.add_argument('--disable-blink-features=AutomationControlled') # Убираем сигнатуру Selenium
options.add_argument('--headless')  # Запуск в фоновом режиме
options.add_argument('--disable-gpu')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
driver = webdriver.Chrome(options=options)

baseurl = 'https://quotes.toscrape.com/'



def wait_for_data(css_selector, prev_tag, timeout=2):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.find_element(By.CSS_SELECTOR, css_selector).text != prev_tag
        )
    except Exception as e:
        print(f"Timeout: Data did not change within {timeout} seconds.")



if __name__ == '__main__':

    quotes_list = []

    driver.get('https://quotes.toscrape.com/search.aspx')


    dropdown_tags = Select(driver.find_element(By.NAME, "tag"))
    options = dropdown_tags.options
    initial_tag_count = len(options)

    dropdown_authors = Select(driver.find_element(By.NAME, "author"))
    options = dropdown_authors.options
    num_authors = len(options)

    unique_quotes = set()
    list_quotes = []
    prev_tag = ''
    for i in range(1, num_authors):
        dropdown_authors = Select(driver.find_element(By.NAME, "author"))
        dropdown_authors.select_by_index(i)

        WebDriverWait(driver, 20).until(
            lambda d: len(Select(d.find_element(By.NAME, "tag")).options) != initial_tag_count
        )
        dropdown_tags = Select(driver.find_element(By.NAME, "tag"))
        num_tags = len(dropdown_tags.options)

        citations = []
        for j in range(1, num_tags):
            dropdown_tags = Select(driver.find_element(By.NAME, "tag"))
            dropdown_tags.select_by_index(j)
            search_button = driver.find_element(By.NAME, "submit_button")
            search_button.click()

            wait_for_data('span.tag', prev_tag)

            text = driver.find_element(By.CSS_SELECTOR, "span.content").text
            author = driver.find_element(By.CSS_SELECTOR, "span.author").text
            tag = driver.find_element(By.CSS_SELECTOR, "span.tag").text

            prev_tag = tag

            print("text:", text)
            print("author:", author)
            print("tag:", tag)

            quote = {
                "autors": author,
                "text": text,
                "tags": tag,
            }

            if quote["text"] not in unique_quotes:
                unique_quotes.add(quote["text"])
                list_quotes.append(quote)





    driver.quit()

    df = pd.DataFrame(list_quotes)
    df.to_excel('quotes.xlsx', index=False)