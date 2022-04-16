import json
from random import randrange

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
    "upgrade-insecure-requests": "1"
}

cookie = {
    "age_confirmed": "Y",
    "_userRegionInfoId": "34",
    "mainShop": '{"cityId":"299","id":"5187","xml_id":"5187"}',
    "price-not-offer": 'Y'

}


def get_catalog(url):
    driver = webdriver.Chrome(executable_path="D:/sel/chromedriver.exe")
    driver.maximize_window()
    try:
        driver.get(url)
        driver.add_cookie({'name': 'age_confirmed', 'value': 'Y'})
        driver.add_cookie({'name': '_userRegionInfoId', 'value': '34'})
        driver.add_cookie({'name': 'price-not-offer', 'value': 'Y'})
        agree_key = driver.find_element(By.XPATH, '//a[@class="button" and @onclick="agree($(this))"]')
        agree_key.click()
        # close_city = (By.XPATH, '//button[@class="fancybox-close-small"]')
        # close_city.click()
        while True:
            if not driver.find_element(By.CLASS_NAME, 'load-more'):
                break
            else:
                actions = ActionChains(driver)
                actions.send_keys(Keys.PAGE_DOWN)
                actions.perform()
                time.sleep(1)
    except Exception as _ex:
        print(_ex)
    finally:
        with open("D:/sel/source-page.html", "w", encoding='utf8') as file:
            file.write(driver.page_source)
        driver.close()
        driver.quit()


def get_wares_urls(file_path):
    with open(file_path, encoding='utf8') as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    wares_url = soup.find_all('div', class_='catalog__item')
    urls = []
    for ware in wares_url:
        ware_url = ware.find("div", class_='product__item parent').find('a').get('href')
        urls.append("https://millstream-wines.ru" + ware_url)
    with open("D:/sel/wares_urls2.txt", "w") as file:
        for url in urls:
            file.write(f"{url}\n")


def get_wares_json(file_path):
    with open(file_path) as file:
        urls_list = [url.strip() for url in file.readlines()]
    result_list = []
    total = len(urls_list)
    count = 1
    for url in urls_list:
        response = requests.get(url, headers=headers, cookies=cookie)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, features="html.parser")
            try:
                name = soup.find('h1').text + ' ' + soup.find('div', class_='card-top__subtitle').text
            except Exception as _ex:
                name = None
            try:
                price = soup.find("div", class_='price--current retail-price').text
            except Exception as _ex:
                price = None
            result_list.append({
                "URL": url,
                "Название": name,
                "Цена": price
            })
            print(f"Обработана позиция {count} из {total}")
            time.sleep(randrange(1, 5))
        else:
            print(f'[ERR] Сайт вернул код ответа {response.status_code}, пропускаем позицию {count}')
        count += 1
    with open('D:/sel/result.json', 'w', encoding='utf8') as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)
    print("[INFO] Запись завершена")


def main():
    get_catalog(url='https://srt.millstream-wines.ru/catalog/')
    get_wares_urls("D:/sel/source-page.html")
    get_wares_json("D:/sel/wares_urls2.txt")


if __name__ == '__main__':
    main()
