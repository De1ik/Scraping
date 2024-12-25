import requests
from bs4 import BeautifulSoup
import pandas as pd

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
    # print("AuthorLink:", baseurl + author_link.get('href'))
    # print("Tags:", all_tags_text)

    return quote


quotes_list = []
for i in range(1, 11):
    response = requests.get(f'https://quotes.toscrape.com/page/{i}/')
    soup = BeautifulSoup(response.text, 'html.parser')
    all_quotes = soup.find_all('div', class_='quote')
    for quote_tag in all_quotes:
        quote = parse_quote(quote_tag)
        quotes_list.append(quote)

    print(f"Page {i} complete: {len(quotes_list)}")


df = pd.DataFrame(quotes_list)
df.to_excel('quotes.xlsx', index=False)
