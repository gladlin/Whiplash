from copy import copy
from abc import ABC, abstractmethod


import undetected_chromedriver


# Абстрактный класс для магазинов.
# Имеет общую для всех магазинов структуру и
# внедрение зависимости драйвера, который для всех одинаковый.
class WebSiteForParsing(ABC):
    def __init__(self, shop_name, driver, shop_main_link, encoding):
        self.shop_name: str = shop_name
        self.__driver__: undetected_chromedriver.Chrome = copy(driver)
        self.__shop_main_link__: str = shop_main_link
        self.__encoding__: str = encoding

    @abstractmethod
    def parse_search_page_without_filters(self, query):
        pass

    @abstractmethod
    def cherrypick_of_parsed_search_page_without_filters(self):
        pass

    @abstractmethod
    def save_result_to_html(self, results):
        pass

    def driver_close_and_quit(self):
        print("\n*** Начало работы метода driver_close() ***")
        if self.__driver__:
            self.__driver__.close()
            self.__driver__.quit()
        print("*** Начало работы метода driver_close() ***\n")

"""
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⡀⠄⠄⠄⠄⠄⠄⠄
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⡀⠄⠄⠄⠄⠄
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠄⠄⠄⠄
⣿⣿⣿⠟⠋⠁⣀⣀⡈⠙⣿⣿⣿⣿⡿⠿⠿⠿⠿⢡⣤⣄⡈⠙⢧⠄⠄⠄
⣏⣉⣀⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠷⠶⠶⠤⣉⠙⠷⣼⣇⠄⠄
⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⡀⠄⠄⣿⣿⣶⣈⠙⣄⠄
⣿⣷⡶⠶⠶⠶⠒⠂⠄⠈⣽⣿⣿⣿⣿⣿⣿⣿⣿⣆⠄⣿⣿⣷⡶⠖⠄⣶
⣁⣤⣴⣶⣶⠾⠟⠛⠛⢛⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄⣿⣿⣿⣓⠂⠄⣤
⠟⢛⣉⣥⣤⣶⡶⠛⢋⣉⡴⢟⣙⠶⣋⣿⣿⣿⠿⠛⠄⠛⠻⢧⡙⠾⢂⣄
⣾⣿⣿⡿⠓⣀⠐⠲⠞⣡⣶⠟⢁⣴⠽⠛⣉⣠⣶⣿⣿⣿⣶⣤⠉⣠⣌⠻
⣿⣿⣫⣶⣾⣿⡟⣠⣤⣤⠄⣀⣤⣤⣴⣾⣿⣿⣿⣿⣿⣿⡿⢋⡄⢻⣿⣷
"""