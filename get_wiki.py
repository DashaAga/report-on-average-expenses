import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.5.810 Yowser/2.5 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest",
    "Accept": 'application/json; charset=utf-8; profile="https://www.mediawiki.org/wiki/Specs/Summary/1.2.0"'
}
def get_data():
    req = requests.get(url="https://en.wikipedia.org/wiki/ISO_4217", headers=headers)

    with open("page.html", "w", encoding="utf-8") as file:
        file.write(req.text)
    with open("page.html", "rb") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    table = soup.find("table", class_='wikitable sortable collapsible')
    print(table)

    currency_codes = table.find_all('td')[::5]
    number_codes = table.find_all('td')[1::5]
    titles = table.find_all('td')[3::5]

    clean_currency_codes = []
    clean_number_codes = []
    clean_titles = []
    for currency_code, number_code, title in zip(currency_codes, number_codes, titles):
        clean_currency_code = str(currency_code).split('>')[1].split('<')[0]
        clean_currency_codes.append(clean_currency_code)

        clean_number_code = str(number_code).split('>')[1].split('<')[0]
        clean_number_codes.append(clean_number_code)

        if 'title' in str(title):
            refined_string = re.findall('title="(.+?)"', str(title))
            clean_titles.append(refined_string[-1])
        else:
            refined_string = str(title).split('>')[1].split('<')[0]
            clean_titles.append(refined_string)

    wiki_table = pd.DataFrame(
        {'num_code': clean_number_codes, 'currency_code': clean_currency_codes, 'title': clean_titles},
        columns=['num_code', 'currency_code', 'title'])
    wiki_table.to_csv('currency_codes_wiki.csv', index=False)

def main():
    get_data()

if __name__=="__main__":
    main()