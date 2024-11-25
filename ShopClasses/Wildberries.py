import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from pprint import pprint

import json

from AbstractClasses.WebSiteForParsing import  WebSiteForParsing


"""
уже злая и все ненавижу но код допилила, доделывать JSON не буду, мне не до этого было
у меня в семье поминки бабушки были вообще блять, весь день никакая
так еще и рейтинг оказывается никому не нужен и ориентируемся чисто на то, что на вб так сделано, поэтому остальное не важно
мне например необязательно рейтинг 4.7 нужен, мне и 4.5 достаточно, есть те, кому например чисто 5.0 надо, на это видимо пофиг
хотя это вообще легко в мобилках сделать
дима, если ты это читаешь, то не надо об этом комментарии писать в чат, не хочу эту всю тему поднимать, не в настроении
я устала ня пока
"""


# Класс для парсинга магазина Wildberries.
class Wildberries(WebSiteForParsing):
    def __init__(self, shop_name, driver, shop_main_link, encoding):
        super().__init__(shop_name, driver, shop_main_link, encoding) # Переопределение полей родительского класса.

    def apply_filters(self, price_from=None, price_to=None, delivery_time=None):
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

    def parse_filtered_items(self, min_rating=None):
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
                        "Название": title,
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
        return results

    def parse_reviews_and_rating(self, item):
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
            return None, 0

    def parse_search_page_without_filters(self, query):
        self.__driver__.get( self.__shop_main_link__ )
        print(f"*** Открыт сайт {self.shop_name} ***")

        try:
            (
                WebDriverWait(self.__driver__, 10.0)
                    .until(
                        EC.presence_of_element_located((By.ID, "searchInput"))
                    )
            )
            print("*** Поисковая строка найдена. Вводим запрос... ***")
        except Exception as e:
            print(f"*** Поисковая строка не найдена. Ошибка {e} ***")


        search_box = self.__driver__.find_element(By.ID, "searchInput")
        search_box.click()
        time.sleep(0.5)
        search_box.click()

        time.sleep(0.2)
        for char in str(query):
            search_box.send_keys(str(char))
            time.sleep(0.15)
        search_box.send_keys(Keys.ENTER)

        next_url = str(self.__driver__.current_url)
        self.__driver__.get( next_url )
        print( next_url )
        time.sleep(1)


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
            print("*** Результаты поиска загрузились ***")
        except Exception as e:
            print(f"***Ошибка до page_debug.html {e} ***")

        with open(f"page_debug_{self.shop_name}.html", "w",
                  encoding=self.__encoding__) as f:
            f.write(self.__driver__.page_source)
            f.close()
        print(f"*** HTML текущей страницы сохранён в 'page_debug_{self.shop_name}.html' ***")

    def cherrypick_of_parsed_search_page_without_filters(self):
        pass

    def parse_item_details(self, link):
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
            return {"Полное описание": "Ошибка при обработке", "Изображение": "Нет изображения"}


    def save_result_to_html(self, results):
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
        html_content += "</table></body></html>"

        with open(filename, "w", encoding=self.__encoding__) as file:
            file.write(html_content)
            print(f"Результаты сохранены в {filename}")

    def driver_close(self):
        self.__driver__.close()
