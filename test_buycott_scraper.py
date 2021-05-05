#!/usr/bin/env python3
"""
This test tests the Buycott web page from where we are scraping product information.
The tests should fail if the page structure changed
"""

import unittest
from buycott_scraper import BuycottScraper
import bs4


class TestBuycottScraper(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        ean_code = "7622300336738".encode("utf-8")
        cls.bs4_soup = ""
        cls.buycott_scraper = BuycottScraper(ean_code)
        cls.product_name = ""
        cls.product_ean = 0
        cls.bs4_soup = cls.buycott_scraper.get_soup()
        cls.soup_list = []

    def test_init(self):
        """
        Tests that the object gets only initiated with a EAN code
        consisting out of numbers
        """
        self.assertIsInstance(self.buycott_scraper, BuycottScraper)
        self.assertIsInstance(self.buycott_scraper.product, dict)
        self.assertIsInstance(self.buycott_scraper.product["ean"], int)
        assert self.buycott_scraper.product["ean"] == 7622300336738

    def test_get_soup(self):
        self.bs4_soup = self.buycott_scraper.get_soup()
        assert isinstance(self.bs4_soup, bs4.BeautifulSoup)

    def test_get_product_name(self):
        name = self.buycott_scraper.get_product_name(self.bs4_soup)
        assert isinstance(name, str)
        assert name == "Oreo Original"

    def test_product_info_table(self):
        self.soup_list = self.buycott_scraper.product_info_table(self.bs4_soup)
        assert isinstance(self.soup_list, bs4.element.Tag)

    def test_get_product_brand(self):
        brand_name = self.buycott_scraper.get_product_brand(
            self.buycott_scraper.pars_info_table(
                self.buycott_scraper.product_info_table(self.bs4_soup)
            )
        )
        assert isinstance(brand_name, str)
        assert brand_name == "Oreo"

    def test_get_product_image(self):
        img_url = self.buycott_scraper.get_product_image(self.bs4_soup)
        assert isinstance(img_url, str)
        assert img_url == "https://s3.amazonaws.com/buycott/images/attachments/000/860/544/w_thumb/d3c9cd5075828624da156ddbcf2c8df3?1398459580"

    def test_scrape(self):
        product = self.buycott_scraper.scrape()
        assert isinstance(product, dict)
        assert product["name"] == "Oreo Original"


if __name__ == "__main__":
    unittest.main()
