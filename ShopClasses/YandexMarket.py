import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from pprint import pprint

# TODO: Сделать метод для возвращения JSON объекта.
import json

from AbstractClasses.WebSiteForParsing import  WebSiteForParsing

class YandexMarket(WebSiteForParsing):
    def __init__(self, shop_name, driver, shop_main_link, encoding):
        super().__init__(shop_name, driver, shop_main_link, encoding)

    def parse_search_page_without_filters(self, query):
        self.__driver__.get( self.__shop_main_link__ )
        print(f"*** Открыт сайт {self.shop_name} ***")

