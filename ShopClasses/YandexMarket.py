import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from pprint import pprint

# TODO: Возможно в будущем его реализовать.

from AbstractClasses.WebSiteForParsing import  WebSiteForParsing

class YandexMarket(WebSiteForParsing):
    def __init__(self, shop_name, driver, shop_main_link, encoding):
        super().__init__(shop_name, driver, shop_main_link, encoding)

    def parse_search_page_without_filters(self, query):
        self.__driver__.get( self.__shop_main_link__ )
        print(f"*** Открыт сайт {self.shop_name} ***")

        try:
            (
                WebDriverWait(self.__driver__, 20.0)
                    .until(
                        EC.presence_of_element_located((By.ID, "header-search")) # Поиск строки поиска на Wildberries.
                    )
            )
            print("*** Поисковая строка найдена. Вводим запрос... ***")
        except Exception as e:
            print(f"*** Поисковая строка не найдена. Ошибка {e} ***")

        search_box = self.__driver__.find_element(By.ID, "header-search")
        search_box.click()
        time.sleep(0.5)
        search_box.click()

        time.sleep(0.2)
        for char in str(query):
            search_box.send_keys(str(char))
            time.sleep(0.15)
        search_box.send_keys(Keys.ENTER)

        next_url = str(self.__driver__.current_url)
        self.__driver__.save_screenshot(f"screenshot_{self.shop_name}_before.png")
        self.__driver__.get(next_url)
        print(next_url)
        time.sleep(1)
        self.__driver__.save_screenshot(f"screenshot_{self.shop_name}_after.png")

        print("*** Запрос отправлен. Ожидаем загрузки результатов... ***")

        try:
            (
                WebDriverWait(self.__driver__, 45.0)
                .until(
                    lambda d: d.execute_script(
                        "return document.querySelectorAll('.product-card__wrapper')"
                    )
                )
            )
            self.__driver__.save_screenshot("Aboba_Wildberries_WebDriverWait.png")
            print("*** Результаты поиска загрузились ***")
        except Exception as e:
            self.__driver__.save_screenshot("NeAboba_Wildberries_WebDriverWait.png")
            print(f"***Ошибка до page_debug.html {e} ***")

        with open(f"page_debug_{self.shop_name}.html", "w",
                  encoding=self.__encoding__) as f:  # Файл, в котором прям вся страница с поиском по запросу, городом новосибом родненьким и еще чем-то может быть
            f.write(self.__driver__.page_source)
            f.close()
        print(f"*** HTML текущей страницы сохранён в 'page_debug_{self.shop_name}.html' ***")

    def cherrypick_of_parsed_search_page_without_filters(self):
        print("*** Конец работы метода cherrypick_of_parsed_search_page_without_filters() ***")

    def save_result_to_html(self, results):
        print("*** Конец работы метода save_result_to_html() ***")