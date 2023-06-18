import requests
import img2pdf


def gathering_urls():
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    all_pages = []
    for i in range(1, 49):
        url = f"https://www.recordpower.co.uk/flip/Winter2020/files/mobile/{i}.jpg"
        response = requests.get(url=url, headers=headers)

        with open(f'content/page_{i}.jpg', 'wb') as f:
            f.write(response.content)
            all_pages.append(f'content/page_{i}.jpg')
        print(f'Downloaded {i} from 48')

    with open('content.pdf', 'wb') as f:
        f.write(img2pdf.convert(all_pages))

    print('Ended with success')


def main():
    gathering_urls()


if __name__ == '__main__':
    main()