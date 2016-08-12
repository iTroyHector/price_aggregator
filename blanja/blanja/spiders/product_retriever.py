import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from blanja.conf.settings import conf
from blanja.exceptions.product_retriever_exceptions import (
        SearchInputNotFound,
        SearchButtonNotFound,
        ElementNotClickeable
        )
class ProductsSpider(scrapy.Spider):
    name = "blanja"
    
    def start_requests(self):
        self._set_up_driver()
        self._load_website("http://www.blanja.com")
        response = self._make_search()
        yield response

    def parse(self, response):
        pass

    def _set_up_driver(self):
        chrome_driver = conf.get("selenium_data", "chrome_driver")
        self.driver = webdriver.Chrome(chrome_driver)

    def _load_website(self, url):
        self.driver.get(url)

    def _make_search(self, input_id="itemSearchKeyWords",
            button_id="itemSearchBtn", product_name="Iphone 6S"):
        #import pdb; pdb.set_trace()
        try:
            element = self.driver.find_element_by_id(input_id)
        except NoSuchElementException:
            raise SearchInputNotFound
        element.send_keys(product_name)
        try:
            button_search = self.driver.find_element_by_id("itemSearchBtn")
        except NoSuchElementException:
            raise SearchButtonNotFound
        try:
            button_search.click()
        except Exception:
            raise ElementNotClickeable
        url = str(self.driver.current_url)
        headers = {}
        return scrappy.http.Response(url=url,
                body=self.driver.page_source
                )
