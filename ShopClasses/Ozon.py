import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpCond
from bs4 import BeautifulSoup
from pprint import pprint

# TODO: Сделать метод для возвращения JSON объекта.
import json

from AbstractClasses.WebSiteForParsing import  WebSiteForParsing


class Ozon(WebSiteForParsing):
    def __init__(self, shop_name, driver, shop_main_link, encoding):
        super().__init__(shop_name, driver, shop_main_link, encoding)

    def parse_search_page_without_filters(self, query):
        self.__driver__.get( self.__shop_main_link__ )
        self.__driver__.save_screenshot(f"screenshot_{self.shop_name}.png")

        print(f"*** Открыт сайт {self.shop_name} ***")

        # pprint(
        #     self.__driver__.page_source
        # )
        with open(f"page_debug_{self.shop_name}.html", "w",
                  encoding=self.__encoding__) as f:  # Файл, в котором прям вся страница с поиском по запросу, городом новосибом родненьким и еще чем-то может быть
            f.write(self.__driver__.page_source)
            f.close()

        (
            WebDriverWait(self.__driver__, 30.0)
                .until(
                    ExpCond.presence_of_element_located((By.CSS_SELECTOR, "jaa0_33"))
                )
        )
        print("*** Поисковая строка найдена. Вводим запрос... ***")

        # search_box = self.__driver__.find_element(By.CLASS_NAME, "jaa0_33")

        time.sleep(2)
        search_box = self.__driver__.find_element(By.CSS_SELECTOR, "jaa0_33")
        search_box.click()
        search_box.send_keys(str(query) + Keys.ENTER)
        self.__driver__.save_screenshot(f"screenshot_{self.shop_name}_1.png")

        print("*** Запрос отправлен. Ожидаем загрузки результатов... ***")
        (
            WebDriverWait(self.__driver__, 60.0)
                .until(
                    lambda script: script.execute_script(
                        "return document.querySelectorAll('.sj6_23')"
                    )
                )
        )
        print("*** Результаты поиска загрузились ***")

        # with open(f"page_debug_{self.shop_name}.html", "w",
        #           encoding=self.__encoding__) as f:  # Файл, в котором прям вся страница с поиском по запросу, городом новосибом родненьким и еще чем-то может быть
        #     f.write(self.__driver__.page_source)
        #     f.close()
        print(f"*** HTML текущей страницы сохранён в 'page_debug_{self.shop_name}.html' ***")

    def cherrypick_of_parsed_search_page_without_filters(self):
        pass

    def save_result_to_html(self, results):
        # filename = f"index_{self.shop_name}.html"
        # html_content = """
        #             <html>
        #             <head><title>Результаты поиска</title></head>
        #             <body>
        #             <h1>Результаты поиска</h1>
        #             <table border="1">
        #                 <tr>
        #                     <th>Название</th>
        #                     <th>Цена</th>
        #                     <th>Рейтинг</th>
        #                     <th>Ссылка</th>
        #                 </tr>
        #             """
        # for result in results:
        #     html_content += f"""
        #                 <tr>
        #                     <td>{result["Название"]}</td>
        #                     <td>{result["Цена"]}</td>
        #                     <td>{result["Рейтинг"]}
        #                     <td><a href="{result["Ссылка"]}" target="_blank">Ссылка</a></td>
        #                 </tr>
        #                 """
        # else:
        #     html_content += f"""
        #                 <p>Обрыв цикла обработки и добавления элементов из списка результатов в html-таблицу</p>
        #                 """
        #
        # html_content += """
        #             </table>
        #             </body>
        #             </html>
        #             """
        # with open(filename, "w", encoding=self.__encoding__) as file:
        #     file.write(html_content)  # Запись HTML-разметки результатов для удобства анализирования.
        #     file.close()
        #     print(f"*** Результаты записаны в {filename} ***")
        pass

    def driver_close(self):
        self.__driver__.close()
