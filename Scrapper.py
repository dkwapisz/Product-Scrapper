import json

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'PostmanRuntime/7.36.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive'
}


def get_price_from_site_1():
    url = "https://www.douglas.pl/pl/p/3001036324"
    response = requests.get(url, params={"variant": "973088"}, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        scripts = soup.find_all('script', {'type': 'application/ld+json'})
        for script in scripts:
            data = json.loads(script.string)
            for item in data:
                if "@type" in item and item["@type"] == "Product":
                    return "Douglas " + str(item["offers"]["price"]) + " PLN - " + url
    else:
        raise ValueError(f'Error fetching the page, status code: {response.status_code}, url: {response.reason}')


def scrape_prices():
    prices = {
        'Site 1': [],
        #'Site 2': [],
    }

    prices['Site 1'].append(get_price_from_site_1())
    #prices['Site 2'].append(get_price_from_site_2())

    return prices


def generate_report(scrapped_prices):
    with open('prices_report.txt', 'w') as file:
        for site, price_list in scrapped_prices.items():
            for price in price_list:
                file.write(f"{price}\n")
            file.write("\n")


if __name__ == "__main__":
    prices = scrape_prices()
    generate_report(prices)
