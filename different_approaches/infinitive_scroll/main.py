from bs4 import BeautifulSoup
from selenium import webdriver

import pandas as pd
import time



options = webdriver.ChromeOptions()
# options.add_argument('--disable-blink-features=AutomationControlled') # Убираем сигнатуру Selenium
# options.add_argument('--headless')  # Запуск в фоновом режиме
# options.add_argument('--disable-gpu')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
driver = webdriver.Chrome(options=options)

baseurl = 'https://quotes.toscrape.com/'
url = 'https://quotes.toscrape.com/scroll'


# Scroll and collect data
def scroll_down():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html = driver.page_source
    driver.quit()
    return html


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
    driver.get(url)
    html = scroll_down()
    soup = BeautifulSoup(html, 'html.parser')

    all_quotes = soup.find_all('div', class_='quote')
    print(f"Amount of quotes: {len(all_quotes)}")

    quotes_list = []
    for quote_tag in all_quotes:
        quote = parse_quote(quote_tag)
        quotes_list.append(quote)

    df = pd.DataFrame(quotes_list)
    df.to_excel('quotes.xlsx', index=False)


