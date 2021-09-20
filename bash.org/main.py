import json
import os

import requests
from bs4 import BeautifulSoup

import time


def get_all_quotes():
    url = 'https://bash.im/'
    headers = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko)"
                      " Chrome / 92.0.4515.159 Safari / 537.36"
    }
    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")
    # quotes = soup.find_all("article", class_="quote")
    pages_number = int(soup.find("div", class_="pager").find("input", class_='pager__input').get("max"))
    quotes_exist = []
    quotes_loaded = None
    try:
        with open('bash.json', 'r', encoding='utf8') as file:
            quotes_loaded = json.load(file)
        for i in range(len(quotes_loaded)):
            quotes_exist.append(quotes_loaded[i]['quote_num'])
    except Exception as e:
        print(e)
    q = []
    quotes_count = 0
    for j in range(1, pages_number):
        url = f'https://bash.im/index/{j}'
        print(f'Читаем {url}  из {pages_number}')
        res = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(res.text, "lxml")
        quotes = soup.find_all("article", class_="quote")
        for i in range(len(quotes)):
            quote = quotes[i].find("div", class_='quote__body').get_text(strip=True, separator='\n')
            quote_date = quotes[i].find("div", class_="quote__header_date").get_text()
            quote_url = f'https://bash.im{quotes[i].find("a", class_="quote__header_permalink").get("href")}'
            quote_num = quote_url[22:]
            # quote_num = quotes[i].find("article", class_="quote").get("data-quote")
            if quote_num not in quotes_exist:
                q.append({"quote_num": quote_num,
                          "quote_date": quote_date,
                          "quote_url": quote_url,
                          "quote": quote})
                quotes_count += 1
        print(f"Добавили {quotes_count} цитат")
        time.sleep(1)
    if quotes_count > 0:
        with open('bash.json', 'a', encoding='utf8') as file:
            json.dump(q, file, indent=4, ensure_ascii=False)
    return "DONE"


def get_all_quotes_num():
    url = 'https://bash.im/'
    headers = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko)"
                      " Chrome / 92.0.4515.159 Safari / 537.36"
    }
    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")
    # # quotes = soup.find_all("article", class_="quote")
    pages_number = int(soup.find("div", class_="pager").find("input", class_='pager__input').get("max"))
    # pages_number = 2
    quotes_exist = []
    quotes_loaded = []
    try:
        with open('bash.json', 'r', encoding='utf8') as file:
            quotes_loaded = json.load(file)
        for i in range(len(quotes_loaded)):
            quotes_exist.append(quotes_loaded[i]['quote_num'])
    except Exception as e:
        print(e)
    quotes_count = 0
    for j in range(1, pages_number):
        url = f'https://bash.im/index/{j}'
        print(f'Читаем {url}  из {pages_number}')
        res = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(res.text, "lxml")
        quotes_on_page = soup.find_all("article", class_="quote")
        for i in reversed(range(len(quotes_on_page))):
            quote_num = quotes_on_page[i].get('data-quote')
            if quote_num not in quotes_exist:
                quotes_loaded.append({"quote_num": quote_num})
                quotes_count += 1
        print(f"Добавили {quotes_count} цитат")
        time.sleep(1)
    if quotes_count > 0 and os.path.isfile('bash.json'):
        with open('bash.json', 'r+', encoding='utf8') as file:
            file.seek(0)
            json.dump(quotes_loaded, file, indent=4, ensure_ascii=False)
    else:
        with open('bash.json', 'w', encoding='utf8') as file:
            json.dump(quotes_loaded, file, indent=4, ensure_ascii=False)
    return "DONE"


def get_new_quotes():
    url = 'https://bash.im/'
    headers = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko)"
                      " Chrome / 92.0.4515.159 Safari / 537.36"
    }
    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")
    quotes_exist = []
    quotes_loaded = []
    try:
        with open('bash.json', 'r', encoding='utf8') as file:
            quotes_loaded = json.load(file)
        for i in range(len(quotes_loaded)):
            quotes_exist.append(quotes_loaded[i]['quote_num'])
    except Exception as e:
        print(e)
    quotes_count = 0
    quotes_on_page = soup.find_all("article", class_="quote")
    for i in reversed(range(len(quotes_on_page))):
        quote_num = quotes_on_page[i].get('data-quote')
        if quote_num not in quotes_exist:
            quotes_loaded.append({"quote_num": quote_num})
            quote = quotes_on_page[i].find("div", class_='quote__body').get_text(strip=True, separator='\n')
            quote_url = f'https://bash.im{quotes_on_page[i].find("a", class_="quote__header_permalink").get("href")}'
            print(f"Цитата №{quote_num}, {quote_url} \n")
            print(quote)
            print('#'*30+'\n')
            quotes_count += 1
    if quotes_count > 0 and os.path.isfile('bash.json'):
        with open('bash.json', 'r+', encoding='utf8') as file:
            print(f"Добавили {quotes_count} цитат")
            file.seek(0)
            json.dump(quotes_loaded, file, indent=4, ensure_ascii=False)
    elif quotes_count == 0:
        print("Нет новых цитат")
    return "DONE"


def get_random_quotes():
    url = 'https://bash.im/random'
    headers = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko)"
                      " Chrome / 92.0.4515.159 Safari / 537.36"
    }
    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")
    quotes_on_page = soup.find_all("article", class_="quote")
    for i in range(len(quotes_on_page)):
        quote_date = quotes_on_page[i].find("div", class_="quote__header_date").get_text(strip=True, separator='')
        quote_num = quotes_on_page[i].get('data-quote')
        quote = quotes_on_page[i].find("div", class_='quote__body').get_text(strip=True, separator='\n')
        quote_url = f'https://bash.im{quotes_on_page[i].find("a", class_="quote__header_permalink").get("href")}'
        print(f"Цитата №{quote_num} от {quote_date}, {quote_url} \n")
        print(quote)
        print('#' * 30 + '\n')
    return "DONE"


def main():
    if not os.path.isfile('bash.json'):
        os.mknod('bash.json')
    get_all_quotes_num()
    get_new_quotes()
    get_random_quotes()


if __name__ == '__main__':
    main()
