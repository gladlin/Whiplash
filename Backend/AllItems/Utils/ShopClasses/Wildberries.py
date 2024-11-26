import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# TODO: Сделать метод для возвращения JSON объекта.

from Backend.AllItems.Utils.AbstractClasses.WebSiteForParsing import  WebSiteForParsing


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
        search_box = None
        try:
            # (
            #     WebDriverWait(self.__driver__, 20.0)
            #         .until(
            #             EC.presence_of_element_located((By.ID, "searchInput")) # Поиск строки поиска на Wildberries.
            #         )
            # )

            # search_box = self.__driver__.find_element(By.ID, "searchInput")
            search_box = WebDriverWait(self.__driver__, 20.0).until( EC.presence_of_element_located((By.ID, "searchInput")) )
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

            time.sleep(1) # Увеличено время ожидания.

        except Exception as e:
            print(f"*** Ошибка при поиске или вводе запроса: {e} ***")
            return -100

        # Парсинг карточек товаров.
        try:
            next_url = str(self.__driver__.current_url)
            # self.__driver__.save_screenshot(f"screenshot_{self.shop_name}_before.png")
            self.__driver__.get(next_url)
            print(next_url)
            time.sleep(1)
            # self.__driver__.save_screenshot(f"screenshot_{self.shop_name}_after.png")
            print("*** Запрос отправлен. Ожидаем загрузки результатов... ***")

            # Берём карточки товаров.
            try:
                # (
                #     WebDriverWait(self.__driver__, 45.0)
                #     .until(
                #         lambda d: d.execute_script(
                #             "return document.querySelectorAll('.product-card__wrapper')"
                #         )
                #     )
                # )
                (
                    WebDriverWait(self.__driver__, 45.0)
                    .until(
                        lambda d:
                            len(d.find_elements(By.CSS_SELECTOR, '.product-card__wrapper')) > 0
                    )
                )
                # self.__driver__.save_screenshot(f"screenshot_{self.shop_name}_WebDriverWait.png")
                print("*** Результаты поиска загрузились ***")

                with open(f"page_debug_{self.shop_name}.html", "w",
                          encoding=self.__encoding__) as f:  # Файл, в котором прям вся страница с поиском по запросу, городом новосибом родненьким и еще чем-то может быть
                    f.write(self.__driver__.page_source)
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
                title_tag = item.select_one("span.product-card__name")
                title = title_tag.text.strip() if title_tag else "Название отсутствует"

                price_tag = item.select_one("ins.price__lower-price")
                price = price_tag.text.strip() if price_tag else "Цена отсутствует"

                rating, reviews_count = self.parse_reviews_and_rating(item)

                link_tag = item.select_one("a")
                link = f"{link_tag['href']}" if link_tag else "Ссылка отсутствует"
                details = self.parse_item_details(link) if link != "Ссылка отсутствует" else {
                    "Полное описание": None,
                    "Изображение": None,
                }

                results.append(
                    {
                        "Название": title[2::],
                        "Цена": price,
                        "Рейтинг": rating if rating is not None else "Нет оценок",
                        "Количество отзывов": reviews_count,
                        "Ссылка": link,
                        "Полное описание": details.get("Полное описание", "Описание отсутствует"),
                        "Изображение": details.get("Изображение", "Нет изображения"),
                    }
                )
            except Exception as e:
                print(f"Ошибка при обработке товара: {e}")

        print("*** Конец работы метода cherrypick_of_parsed_search_page_without_filters() ***\n")
        return results

    def save_result_to_html(self, results):
        print("\n*** Начало работы метода save_result_to_html() ***")

        filename = f"index_{self.shop_name}.html"
        html_content = """
            <html>
        <head>
            <title>Результаты поиска</title>
            <style>
                table {border-collapse: collapse; width: 100%;}
                th, td {border: 1px solid black; padding: 8px; text-align: left;}
                img {max-width: 100px; max-height: 100px;}
            </style>
        </head>
        <body>
        <h1>Результаты поиска</h1>
        <table>
            <tr>
                <th>Название</th>
                <th>Цена</th>
                <th>Рейтинг</th>
                <th>Количество отзывов</th>
                <th>Ссылка</th>
                <th>Полное описание</th>
                <th>Изображение</th>
            </tr>
            """
        for result in results:
            html_content += f"""
                        <tr>
                            <td>{result['Название']}</td>
                            <td>{result['Цена']}</td>
                            <td>{result['Рейтинг']}</td>
                            <td>{result['Количество отзывов']}</td>
                            <td><a href="{result['Ссылка']}" target="_blank">Ссылка</a></td>
                            <td>{result['Полное описание']}</td>
                            <td><img src="{result['Изображение']}" alt="Нет изображения"></td>
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
            print(f"*** Результаты записаны в {filename} ***")

        print("*** Конец работы метода save_result_to_html() ***\n")

    # Часть Алины с моими исправлениями.
    # Применение фильтров.
    def apply_filters(self, price_from=None, price_to=None, delivery_time=None):
        print("\n*** Начало работы метода apply_filters() ***")

        try:
            price_button = WebDriverWait(self.__driver__, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".dropdown-filter__btn--priceU"))
            )
            price_button.click()

            if price_from:
                price_from_input = WebDriverWait(self.__driver__, 10).until(
                    EC.presence_of_element_located((By.NAME, "startN"))
                )
                price_from_input.clear()
                price_from_input.send_keys(str(price_from))

            if price_to:
                price_to_input = WebDriverWait(self.__driver__, 10).until(
                    EC.presence_of_element_located((By.NAME, "endN"))
                )
                price_to_input.clear()
                price_to_input.send_keys(str(price_to))

            confirm_price_button = WebDriverWait(self.__driver__, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class, 'filter-btn__main') and text()='Готово']")
                )
            )
            confirm_price_button.click()

            if delivery_time:
                delivery_button = WebDriverWait(self.__driver__, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".dropdown-filter__btn--fdlvr"))
                )
                delivery_button.click()

                delivery_option = WebDriverWait(self.__driver__, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"//span[text()='{delivery_time}']")
                    )
                )
                delivery_option.click()

        except Exception as e:
            print(f"Ошибка при применении фильтров: {e}")

        print("*** Конец работы метода apply_filters() ***\n")

    def parse_filtered_items(self, min_rating=None):
        print("\n*** Начало работы метода parse_filtered_items() ***")

        soup = BeautifulSoup(self.__driver__.page_source, "html.parser")
        items = soup.select("div.product-card__wrapper")

        results = []
        for item in items:
            try:
                title_tag = item.select_one("span.product-card__name")
                title = title_tag.text.strip() if title_tag else "Название отсутствует"

                price_tag = item.select_one("ins.price__lower-price")
                price = price_tag.text.strip() if price_tag else "Цена отсутствует"

                rating, reviews_count = self.parse_reviews_and_rating(item)

                if min_rating is not None and (rating is None or rating < min_rating):
                    continue

                link_tag = item.select_one("a")
                link = f"{link_tag['href']}" if link_tag else "Ссылка отсутствует"
                details = self.parse_item_details(link) if link != "Ссылка отсутствует" else {
                    "Полное описание": None,
                    "Изображение": None,
                }

                results.append(
                    {
                        "Название": title[2::],
                        "Цена": price,
                        "Рейтинг": rating if rating is not None else "Нет оценок",
                        "Количество отзывов": reviews_count,
                        "Ссылка": link,
                        "Полное описание": details.get("Полное описание", "Описание отсутствует"),
                        "Изображение": details.get("Изображение", "Нет изображения"),
                    }
                )
            except Exception as e:
                print(f"Ошибка при обработке товара: {e}")

        # self.__driver__.save_screenshot("parse_filtered_items.png")
        print("*** Конец работы метода parse_filtered_items() ***\n")
        return results

    def parse_reviews_and_rating(self, item):
        print("\n*** Начало работы метода parse_reviews_and_rating() ***")

        try:
            empty_rating_element = item.select_one(".product-card__count--empty")
            if empty_rating_element:
                return None, 0

            rating_element = item.select_one(".address-rate-mini.address-rate-mini--sm")
            rating = float(rating_element.text.strip().replace(",", ".")) if rating_element else None

            reviews_element = item.select_one(".product-card__count")
            reviews_count = int(reviews_element.text.strip().split()[0]) if reviews_element else 0

            return rating, reviews_count
        except Exception as e:
            print(f"Ошибка при извлечении рейтинга и отзывов: {e}")

        print("*** Конец работы метода parse_reviews_and_rating() ***\n")
        return None, 0

    def parse_item_details(self, link):
        print("\n*** Начало работы метода parse_item_details() ***")

        try:
            self.__driver__.get(link)
            WebDriverWait(self.__driver__, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-page__btn-detail"))
            )

            details_button = self.__driver__.find_element(By.CSS_SELECTOR, ".product-page__btn-detail")
            details_button.click()

            soup = BeautifulSoup(self.__driver__.page_source, "html.parser")
            description_tag = soup.select_one("p.option__text")
            description = description_tag.text.strip() if description_tag else "Описание отсутствует"

            image_tag = soup.select_one("img.photo-zoom__preview")
            image_link = image_tag.get("src", "Нет изображения") if image_tag else "Нет изображения"

            return {"Полное описание": description, "Изображение": image_link}
        except Exception as e:
            print(f"Ошибка при обработке страницы товара: {e}")

        print("*** Конец работы метода parse_item_details() ***\n")
        return {"Полное описание": "Ошибка при обработке", "Изображение": "Нет изображения"}


