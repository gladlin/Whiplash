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
        print("\n*** Начало работы метода parse_search_page_without_filters() ***")
        print(f"*** Открываем сайт {self.shop_name} ***")
        self.__driver__.get( self.__shop_main_link__ )
        print(f"*** Открыт сайт {self.shop_name} ***")  # Print'ы для отслеживания работы программы и debugging'а.

        # Поиск строки поиска.
        try:
            (
                WebDriverWait(self.__driver__, 20.0)
                    .until(
                        EC.presence_of_element_located((By.ID, "searchInput")) # Поиск строки поиска на Wildberries.
                    )
            )

            search_box = self.__driver__.find_element(By.ID, "searchInput")
            print("*** Поисковая строка найдена. Вводим запрос... ***")
            search_box.click()  # Имитация действий пользователя, что когда он хочет ввести что-то в поиск, то он должен нажать на него
            time.sleep(0.5)
            search_box.click()
            time.sleep(0.5)
            search_box.click()
            print(f"Поле ввода {self.shop_name} выбрано?: " + str(search_box.is_selected()))

            time.sleep(0.2)
            for char in str(query):
                search_box.send_keys(str(char))
                time.sleep(0.15)
            search_box.send_keys(Keys.ENTER)
            time.sleep(0.5)
            search_box.send_keys(Keys.ENTER)

            next_url = str(self.__driver__.current_url)
            # self.__driver__.save_screenshot(f"screenshot_{self.shop_name}_before.png")
            self.__driver__.get(next_url)
            print(next_url)
            time.sleep(1)
            # self.__driver__.save_screenshot(f"screenshot_{self.shop_name}_after.png")
            print("*** Запрос отправлен. Ожидаем загрузки результатов... ***")

            # Берём карточки товаров.
            try:
                (
                    WebDriverWait(self.__driver__, 45.0)
                    .until(
                        lambda d: d.execute_script(
                            "return document.querySelectorAll('.product-card__wrapper')"
                        )
                    )
                )
                # self.__driver__.save_screenshot(f"screenshot_{self.shop_name}_WebDriverWait.png")
                print("*** Результаты поиска загрузились ***")

                with open(f"page_debug_{self.shop_name}.html", "w",
                          encoding=self.__encoding__) as f:  # Файл, в котором прям вся страница с поиском по запросу, городом новосибом родненьким и еще чем-то может быть
                    f.write(self.__driver__.page_source)
                    f.close()
                print(f"*** HTML текущей страницы сохранён в 'page_debug_{self.shop_name}.html' ***")

            except Exception as e1:
                # self.__driver__.save_screenshot("NeAboba_Wildberries_WebDriverWait.png")
                print(f"*** Карточки товаров не найдены ***")
                print(e1)

        except Exception as e:
            print(f"*** Поисковая строка не найдена ***")
            print(e)
        finally:
            print("*** Конец работы метода parse_search_page_without_filters() ***\n")

    def cherrypick_of_parsed_search_page_without_filters(self):
        print("\n*** Начало работы метода cherrypick_of_parsed_search_page_without_filters() ***")

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

        print("*** Конец работы метода cherrypick_of_parsed_search_page_without_filters() ***\n")
        return results

    def save_result_to_html(self, results):
        print("\n*** Начало работы метода save_result_to_html() ***")

        filename = f"index_{self.shop_name}.html"
        html_content = f"""
            <html>
            <head><title>Результаты поиска на {self.shop_name}</title></head>
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

        print("*** Конец работы метода save_result_to_html() ***\n")
