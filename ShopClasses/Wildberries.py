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


# Класс для парсинга магазина Wildberries.
class Wildberries(WebSiteForParsing):
    def __init__(self, shop_name, driver, shop_main_link, encoding):
        super().__init__(shop_name, driver, shop_main_link, encoding) # Переопределение полей родительского класса.

    def parse_search_page_without_filters(self, query):
        self.__driver__.get( self.__shop_main_link__ )
        print(f"*** Открыт сайт {self.shop_name} ***")  # Print'ы для отслеживания работы программы и debugging'а.

        (
            WebDriverWait(self.__driver__, 40.0)
                .until(
                    EC.presence_of_element_located((By.ID, "searchInput")) # Поиск строки поиска на Wildberries.
                )
        )
        print("*** Поисковая строка найдена. Вводим запрос... ***")

        search_box = self.__driver__.find_element(By.ID, "searchInput")
        search_box.click()  # Имитация действий пользователя, что когда он хочет ввести что-то в поиск, то он должен нажать на него
        time.sleep(0.3)
        search_box.click()

        time.sleep(0.4)
        for char in str(query):
            search_box.send_keys(str(char))
            time.sleep(0.4)
        search_box.send_keys(Keys.ENTER)

        self.__driver__.save_screenshot(f"screenshot_{self.shop_name}before.png")
        self.__driver__.get( str(self.__driver__.current_url) )
        print(str(self.__driver__.current_url))
        time.sleep(5)
        self.__driver__.save_screenshot(f"screenshot_{self.shop_name}_after.png")

        print("*** Запрос отправлен. Ожидаем загрузки результатов... ***")
        (
            WebDriverWait(self.__driver__, 30.0)
                .until(
                    lambda d: d.execute_script(
                        "return document.querySelectorAll('.product-card__wrapper')"
                    )
        ))
        print("*** Результаты поиска загрузились ***")
        # self.__driver__.save_screenshot(f"screenshot_{self.shop_name}_1.png")

        with open(f"page_debug_{self.shop_name}.html", "w",
                  encoding=self.__encoding__) as f:  # Файл, в котором прям вся страница с поиском по запросу, городом новосибом родненьким и еще чем-то может быть
            f.write(self.__driver__.page_source)
            f.close()
        print(f"*** HTML текущей страницы сохранён в 'page_debug_{self.shop_name}.html' ***")

    def cherrypick_of_parsed_search_page_without_filters(self):
        soup = BeautifulSoup(self.__driver__.page_source, "html.parser")
        items = soup.select("div.product-card__wrapper")

        results = list()
        for item in items:
            try:
                title_tag = item.select_one("span.product-card__name")  # тег с названием товара
                title = title_tag.text.strip() if title_tag else "Название отсутствует"

                price_tag = item.select_one("ins.price__lower-price")  # тег содержанием цены товара(окончательной)
                price = price_tag.text.strip() if price_tag else "Цена отсутствует"

                rating_tag = item.select_one("span.address-rate-mini")  # просто общий рейтинг товара в звездах
                rating = rating_tag.text.strip() if rating_tag else "Рейтинг отсутствует"

                link_tag = item.select_one("a")  # ссылка на саму карточку товара
                link = f"{link_tag['href']}" if link_tag else "Ссылка отсутствует"

                results.append(
                    {
                        "Название": title,
                        "Цена": price,
                        "Рейтинг": rating,
                        "Ссылка": link,
                    }
                )

                # print("*** Результат парсинга (cherrypick) результатов поиска ***")
                # pprint(results)
                # print("*** Конец результата поиска ***")

            except Exception as e:
                print(f"*** Ошибка при обработке товара: {e}! ***")
                continue

        return results

    def save_result_to_html(self, results):
        filename = f"index_{self.shop_name}.html"
        html_content = """
            <html>
            <head><title>Результаты поиска</title></head>
            <body>
            <h1>Результаты поиска</h1>
            <table border="1">
                <tr>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Рейтинг</th>
                    <th>Ссылка</th>
                </tr>
            """
        for result in results:
            html_content += f"""
                <tr>
                    <td>{result["Название"]}</td>
                    <td>{result["Цена"]}</td>
                    <td>{result["Рейтинг"]}
                    <td><a href="{result["Ссылка"]}" target="_blank">Ссылка</a></td>
                </tr>
                """
        else:
            html_content += f"""
                <p>Обрыв цикла обработки и добавления элементов из списка результатов в html-таблицу</p>
                """

        html_content += """
            </table>
            </body>
            </html>
            """
        with open(filename, "w", encoding=self.__encoding__) as file:
            file.write(html_content) # Запись HTML-разметки результатов для удобства анализирования.
            file.close()
            print(f"*** Результаты записаны в {filename} ***")

    def driver_close(self):
        self.__driver__.close()
