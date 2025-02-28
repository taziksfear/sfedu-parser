import requests
from bs4 import BeautifulSoup
import time
from dotenv import load_dotenv
import os
load_dotenv()

api_url = os.getenv('api_url')

def scrape_news_page(news_id):
    url = f'https://sfedu.ru/press-center/news/{news_id}/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    not_found = soup.find('h3', id='titl')
    if not_found and not_found.text.strip() == 'Новость не найдена':
        return None

    title = soup.find('h1').text.strip()
    content = soup.find('div', class_='news-content').text.strip()

    return {'id': news_id, 'title': title, 'content': content}

def scrape_page(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    content_wrapper = soup.find('div', class_='content_wrapper')
    if not content_wrapper:
        print(f'не найденно на странице: {url}')
        return ''

    content = content_wrapper.get_text(separator='\n', strip=True)
    return content

def send_to_api(data):
    try:
        response = requests.post(api_url, json=data)
        response.raise_for_status()
        print(f"все отправленно на апи: {data}")
    except requests.exceptions.RequestException as e:
        print(f"ошибка отправки: {e}")

def main():
    news_id = 77166

    while True:
        news = scrape_news_page(news_id)
        if news:
            print("\nНовостные страницы:")
            print(f"ID: {news['id']}, Title: {news['title']}, Content: {news['content']}")
            send_to_api(news)
            news_id += 1
        else:
            print(f'не найденна страница новостей под ID:{news_id}')

        pages = {
            "Bakolavriat": 'https://sfedu.ru/www/stat_pages22.show?p=ABT/N8206',
            "Magistratura": 'https://sfedu.ru/www/stat_pages22.show?p=ABT/N8207/P',
            "Aspirantura": 'https://sfedu.ru/www/stat_pages22.show?p=ABT/N8210/P',
            "Assisterantura": 'https://sfedu.ru/www/stat_pages22.show?p=ABT/N13437/P',
            "SPO": 'https://sfedu.ru/www/stat_pages22.show?p=ABT/N8209/P'
        }

        for name, url in pages.items():
            content = scrape_page(url)
            if content:
                print(f"\n{name} содержимое страницы:")
                print(content)
            else:
                print(f'не найденно информации на странице: {name}')

        time.sleep(86400)

if __name__ == '__main__':
    main()