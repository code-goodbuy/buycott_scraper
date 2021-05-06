#!/usr/bin/env python3
# *_* coding: utf-8 *_*

import requests
from datetime import datetime, timezone

from bs4 import BeautifulSoup


class BuycottScraper:
    def __init__(self, code):
        ean_code = int(code.decode("utf-8"))
        print(f"Buycott scraper called for {ean_code}")
        self.product = {
            "_id": ean_code,
            "ean": ean_code,
            "user": "60905172b52cca811ac73ad7",
            "verified": True,
            "updated_at": "",
            "corporation": "",
            "scraper_info": {"source": "buycott"},
        }
        self.url = "https://www.buycott.com"
        self.path = "/upc/"
        self.wanted_infos = ("Brand", "Manufacturer", "Country")
        self.soup = ""

    def get_soup(self):
        url = self.url + self.path + str(self.product["ean"])
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

    def get_product_name(self, soup):
        try:
            return soup.find("h2").text
        except Exception as e:
            print("Can't find name. Error: ", str(e))

    def product_info_table(self, soup):
        return soup.find("table", attrs={"class": "table product_info_table"})

    def pars_info_table(self, product_info_table):
        return [
            (td.text, product_info_table("td")[i + 1].text)
            for i, td in enumerate(product_info_table("td"))
            if td.text in self.wanted_infos
        ]

    def get_product_brand(self, soup_list):
        return [tup[1] for tup in soup_list if tup[0] == "Brand"][0]

    def get_product_image(self, soup):
        return soup.find("img").attrs["src"]

    def set_time(self):
        dt = datetime.now(timezone.utc)
        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.timestamp()
        timestamp_str = dt.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        return utc_timestamp, timestamp_str

    def scrape(self):
        soup = self.get_soup()
        self.product["name"] = self.get_product_name(soup)
        self.product["brand"] = self.get_product_brand(
                soup_list=self.pars_info_table(self.product_info_table(soup))
            )
        self.product["utc_time"], self.product["created_at"] = self.set_time()
        self.product["scraped_image"] = self.get_product_image(soup)
        return self.product
