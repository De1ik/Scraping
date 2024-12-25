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


if __name__ == '__main__':


    quotes_list = []
    for i in range(1, 11):
        response = requests.get(f'https://quotes.toscrape.com/tableful/page/{i}/')
        soup = BeautifulSoup(response.text, 'html.parser')
        all_tr = soup.find_all('tr')


        print("Amount of elements:", (len(all_tr) - 2) // 2)

        for j in range(1, len(all_tr) - 1, 2):
            text = all_tr[j].find('td').text
            all_tags = all_tr[j+1].find_all('a')
            all_tags_text = [el.text for el in all_tags]

            quote = {
                'text': text,
                'tags': all_tags_text,
            }

            quotes_list.append(quote)

        print(f"Page {i} complete: {len(quotes_list)}")


    df = pd.DataFrame(quotes_list)
    df.to_excel('quotes.xlsx', index=False)
