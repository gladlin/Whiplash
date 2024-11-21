from abc import ABC, abstractmethod

# Абстрактный класс для магазинов.
# Имеет общую для всех магазинов структуру и
# внедрение зависимости драйвера, который для всех одинаковый.
class WebSiteForParsing(ABC):
    def __init__(self, shop_name, driver, shop_main_link, encoding):
        self.shop_name = shop_name
        self.__driver__ = driver
        self.__shop_main_link__ = shop_main_link
        self.__encoding__ = encoding

    @abstractmethod
    def parse_search_page_without_filters(self, query):
        pass

    @abstractmethod
    def cherrypick_of_parsed_search_page_without_filters(self):
        pass

    @abstractmethod
    def save_result_to_html(self, results):
        pass