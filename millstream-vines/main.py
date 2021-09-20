import json
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
}

cookie = {
    "age_confirmed": "Y",
    "_userRegionId": "34",
    "mainShop": '{"cityId":"299","id":"5187","xml_id":"5187"}'

}


def get_catalog(url):
    driver = webdriver.Chrome(executable_path="D:/sel/chromedriver.exe")
    driver.maximize_window()
    try:
        driver.get(url)
        agree_key = driver.find_element_by_xpath('//a[@class="button" and @onclick="agree($(this))"]')
        agree_key.click()
        close_city = driver.find_element_by_xpath('//button[@class="fancybox-close-small"]')
        close_city.click()
        while True:
            if not driver.find_element_by_class_name('load-more'):
                break
            else:
                actions = ActionChains(driver)
                actions.send_keys(Keys.PAGE_DOWN)
                actions.perform()
                time.sleep(1)
    except Exception as _ex:
        print(_ex)
    finally:
        with open("source-page.html", "w", encoding='utf8') as file:
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
        urls.append("https://millstream-wines.ru"+ware_url)
    with open("wares_urls2.txt", "w") as file:
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
        soup = BeautifulSoup(response.text, 'lxml')
        name = soup.find('h1').text+' '+soup.find('div', class_='card-top__subtitle').text
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
        count += 1
    with open('result.json', 'w', encoding='utf8') as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)
    print("[INFO] Запись завершена")



def main():
    get_catalog(url='https://millstream-wines.ru/catalog/')
    get_wares_urls("source-page.html")
    get_wares_json("wares_urls2.txt")


if __name__ == '__main__':
    main()
