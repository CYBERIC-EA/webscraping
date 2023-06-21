from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
search_term = input("What product do you want to search for? ")

url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

page_text = doc.find(class_="list-tool-pagination-text").strong
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

items_found = {}

for page in range(1, pages + 1):
    url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    div = doc.find(
        class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    items = div.find_all(text=re.compile(search_term))

    for item in items:
        parent = item.parent
        if parent.name != "a":
            continue

        link = parent['href']
        next_parent = item.find_parent(class_="item-container")
        try:
            price = next_parent.find(
                class_="price-current").find("strong").string
            items_found[item] = {"price": int(
                price.replace(",", "")), "link": link}
        except:
            pass

sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])
try:
    if sorted_items[0]:
        print('Y')
except:
    print('empty')

scraped = pd.DataFrame()
name = []
price = []
link = []
for item in sorted_items:

    name.append(item[0])
    price.append(f"${item[1]['price']}")
    link.append(item[1]['link'])

name_series = pd.Series(name, name='Name')
price_series = pd.Series(price, name='Price')
link_series = pd.Series(link, name='Link')

# Concatenate series horizontally
scraped = pd.concat([name_series, price_series, link_series], axis=1)
print(scraped)
