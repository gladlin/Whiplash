import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from pprint import pprint
import re

# TODO: Сделать метод для возвращения JSON объекта.
import json

from AbstractClasses.WebSiteForParsing import  WebSiteForParsing

# Класс для парсинга магазина Пятёрочки.
class Pyatyourochka(WebSiteForParsing):
    def __init__(self, shop_name, driver, shop_main_link, encoding):
        super().__init__(shop_name, driver, shop_main_link, encoding)

    def parse_search_page_without_filters(self, query):
        print("\n*** Начало работы метода parse_search_page_without_filters() ***")
        print(f"*** Открываем сайт {self.shop_name} ***")
        self.__driver__.get( self.__shop_main_link__ )
        print(f"*** Открыт сайт {self.shop_name} ***")

        # self.__driver__.save_screenshot(f"screenshot_{self.shop_name}_OpenSite.png")

        # Поиск строки поиска.
        try:
            (
                WebDriverWait(self.__driver__, 30.0)
                    .until(
                        EC.presence_of_element_located(
                            (By.CLASS_NAME, "W1l53Gki-")
                        )
                    )
            )
            # print("*** Поисковая строка найдена. Вводим запрос... ***")
            # time.sleep(15)
            # self.__driver__.save_screenshot(f"screenshot_{self.shop_name}_BeforeSearchBar1.png")

            search_box = self.__driver__.find_element(By.CLASS_NAME, "W1l53Gki-")
            print("*** Поисковая строка найдена. Вводим запрос... ***")
            # print(f"*** Поисковая строка видна?: {search_box.is_displayed()} ***")
            search_box.click()
            time.sleep(0.5)
            # search_box.click()
            # self.__driver__.save_screenshot(f"screenshot_{self.shop_name}_BeforeSearchBar2.png")

            time.sleep(0.2)
            for char in str(query):
                search_box.send_keys(str(char))
                time.sleep(0.15)
            # self.__driver__.save_screenshot(f"screenshot_{self.shop_name}_BeforeSearchBar3.png")

            # search_box.send_keys(Keys.ENTER + Keys.ENTER)
            (
                WebDriverWait(self.__driver__, 30.0)
                .until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "css-wr8etk")
                    )
                )
            )
            search_button = self.__driver__.find_element(By.CLASS_NAME, "css-wr8etk")
            search_button.click()
            time.sleep(1)
            search_button.click()
            time.sleep(1)
            search_button.click()

            # next_url: str = str( self.__driver__.current_url )
            # self.__driver__.save_screenshot(f"screenshot_{self.shop_name}_before.png")
            # self.__driver__.get( next_url )
            # print( next_url )
            time.sleep(1)
            # self.__driver__.save_screenshot(f"screenshot_{self.shop_name}_after.png")

            print("*** Запрос отправлен. Ожидаем загрузки результатов... ***")

            # Берём карточки товаров.
            try:
                (
                    WebDriverWait(self.__driver__, 20.0)
                        .until(
                            # lambda d: d.execute_script(
                            #     "return document.getElementsByClassName(\"chakra-link xlSVIYdp- css-13jvj27\")"
                            # )
                            EC.presence_of_all_elements_located((By.CLASS_NAME, "xlSVIYdp-"))
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
                print("*** Карточки товаров не найдены ***")
                print(e1)

        except Exception as e:
            print("*** Поисковая строка не найдена ***")
            print(e)
        finally:
            # self.__driver__.save_screenshot(f"screenshot_{self.shop_name}_search_end.png")
            print("*** Конец работы метода parse_search_page_without_filters() ***\n")

    def cherrypick_of_parsed_search_page_without_filters(self):
        print("\n*** Начало работы метода cherrypick_of_parsed_search_page_without_filters() ***")

        results = list()
        try:
            WebDriverWait(self.__driver__, 20.0).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "UEvWGs5b-")
                )
            )
            self.__driver__.save_screenshot("cherrypick_start.png")

            soup = BeautifulSoup(self.__driver__.page_source, 'html.parser')
            groupOfItems = soup.find("div", {"class" : "UEvWGs5b-"} )
            # pprint(groupOfItems.prettify())
            items = groupOfItems.select(".xlSVIYdp-")
            # pprint(items)

            for item in items:
                # print(item.prettify())
                try:
                    image_tag = item.select_one(".jvh9M_6y-")
                    # pprint(image_tag)
                    # print("Голубь")
                    image1 = image_tag['style'] if image_tag is not None \
                        else "None"
                    image = re.search(r"url\(\"(.*?)\"\);", image1).group(1)
                    # print(image)

                    title_tag = item.select_one(".SdLEFc2B-")
                    title = title_tag.text if title_tag is not None \
                        else "None"
                    # print(title)

                    price_123 = item.select(".css-6uvdux")
                    price = (str(price_123[0].text) + "." + str(price_123[1].text)
                             + " " + str(price_123[2].text)) if price_123 else "None"
                    # print(price) if price_123 is not None else "Цены нет"

                    rating_tag = item.select_one(".o1tGK2uB-")
                    raiting = rating_tag.text if rating_tag is not None \
                        else "None"

                    link = self.__shop_main_link__ + str(item['href']) if item is not None \
                        else "None"

                    description_search = self.search_description_of_product(link)
                    description = description_search if description_search is not None \
                        else "None"

                    results.append(
                        {
                            "Название": title,
                            "Цена": price,
                            "Рейтинг": raiting,
                            "Количество отзывов": "None",
                            "Ссылка": link,
                            "Полное описание": description,
                            "Изображение": image,
                        }
                    )
                except Exception as e:
                    print(e)
                    continue

        except Exception as e1:
            print(e1)
            print("*** Ошибка в выделении элементов страницы cherrypick ***")

        # pprint(results)

        print("*** Конец работы метода cherrypick_of_parsed_search_page_without_filters() ***\n")
        return results

    def save_result_to_html(self, results):
        print("\n*** Начало работы метода save_result_to_html() ***")

        filename = f"index_{self.shop_name}.html"
        html_content = f"""
                    <html>
                    <head><title>Результаты поиска на {self.shop_name} </title></head>
                    <body>
                    <h1>Результаты поиска</h1>
                    <table border="1">
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
                            <td>{result["Название"]}</td>
                            <td>{result["Цена"]}</td>
                            <td>{result["Рейтинг"]}</td>
                            <td>{result["Количество отзывов"]}</td>
                            <td><a href="{result["Ссылка"]}" target="_blank">Ссылка</a></td>
                            <td>{result["Полное описание"]}</td>
                            <td><div style='background-image: url(\"{result["Изображение"]}\"); height: 200px;' /></td>

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
            file.write(html_content)  # Запись HTML-разметки результатов для удобства анализирования.
            file.close()
            print(f"*** Результаты записаны в {filename} ***")

        print("*** Конец работы метода save_result_to_html() ***\n")

    def search_description_of_product(self, link: str) -> str:
        print("\n*** Начало работы метода search_description_of_product() ***")

        description = ""
        try:
            time.sleep(1)
            self.__driver__.get(link)
            # print(self.__driver__.current_url)

            WebDriverWait(self.__driver__, 7.0).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".QbszJz8b-"))
            )

            # self.__driver__.save_screenshot(f"k.png")

            soup = BeautifulSoup(self.__driver__.page_source, "html.parser")
            # print(soup.prettify())

            description = soup.select_one(".QbszJz8b-").text
            # pprint(description)

            print("*** Конец работы метода search_description_of_product() ***\n")
            return description
        except Exception as e:
            try:
                WebDriverWait(self.__driver__, 7.0).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".TvoT0wiK-"))
                )

                # self.__driver__.save_screenshot(f"k.png")

                soup = BeautifulSoup(self.__driver__.page_source, "html.parser")
                # print(soup.prettify())

                description = soup.select_one(".TvoT0wiK-").text
                # pprint(description)

                print("*** Конец работы метода search_description_of_product() ***\n")
                return description
            except Exception as e1:
                print(e1)
        print("*** Конец работы метода search_description_of_product() ***\n")
        return None


"""
--------------------------------------------=++**########%%%%####**+==--------------------------====
-----------------------------------------=+*#####%%%%%%%%%%%%%%%%###*+==-------------------------===
--------------------------------------=*##%%%%%%%%%%%%%%%%%%%%%%@%%%##*+=------------------------===
-----------------------------------=+##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*+=--------------------------
--------------------------------=+*##%%%%%%%%%%%%%%%%%%%%%%%%%%%%@@@%%%#*+--------------------------
------------------------------=*#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@@@@@@@@%%#*=------------------------=
----------------------------=*#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@@@@@@@%#*+=-----------------------=
--------------------------=*#%%%%%%%%%%%%%%####################%%%%@@@@%##+=------------------------
------------------------=*#%%%%%%%%%%%%###**********++++===++++++**#%%%%%#=-------------------------
---------------------=+###%%%%%%%%%##****+++++++========----======+++*#%#**+==----------------------
---------------------=*#%%%%%%#*+++++++++=============-------=======+++#%%###*+---------------------
--------------------=*#%%%%%#++++++++++++=============--------========++*%%%%%%*=-------------------
--------------------+####%%#*+=++++++++++=============--------=========++*%@%%%%*=------------------
--------------------*#%%%%#*+==++++++++=============----------=========+++*%%%%%%+------------------
-------------------=*%%%%##*+==+++++++++++==========----------=========++++#@%%%%*=-----------------
------------=======+#%####*+====+++**********++===------------==========+++*%@%%%*=-----------------
--------=========++#####*++====+*##%%%@@%%%%%#*+==-----------======+++===++*#%%%%*=-----------------
------=========+++*#####++===+*#%%%#***####***++==----------=++######**+++++*%@@@#=-----------------
----==========++++*####*+==++*###*+++++******++===---------==+++*##%%%%%#*++*#%@@%+-----------------
--==========+++++**###*+==++***+++************+++==-------=====++++++**#%%***#%%%%+-----------------
==========+++++****###*+++++++++*********#####***++==----===++++++++++++*#%#**#%%%+-----------------
========++++++****####*+++++++*****++++++**#####**+=======+**********+++++#%#*#%%#=-----------------
=======++++++****#####*++++++****+**#####****##**++++=+++**###**+++++**++++*#*#%%*------------------
=====+++++++****######+++++++****#%%%%%%#+*#**#*++++++++++*********+++***++***###+------------------
=====+++++++***#######+====++**###**#%%#*++*###***+++==++++**#*#%%%%%#********##*-------------------
=====+++++++***######*+=====+++*****###**+******++++====+++****#%%%%#%%#**+++*##+-------------------
=====++++++*******###*+======+++++++++++++++++++++++====+++++++******###**+++*##=-------------------
====+++++++**********+=========+++++++++++++++++++++====++++++++++*****++++++*#*=-------------------
====+++++++*****##***+===========++++++++===++++++++====+++++==+++++++++===++*#+--------------------
====+++++++*****##+**+===========+===========+++++++=====+++======+++++++++++***=-------------------
====+++++++*******+**++=====================+**++*****++++++=========++++++++**#+-------------------
===++++++++*******###++++=================++****%@@%###*#%#*+=========+++++++**+=-------------------
===++++++++******#%%#++++++++++++++++++=++++**###%%####**###+==========++++++**+--------------------
===++++++++********##*++++++++++++++++++++++++***#####*****++===========+++++*+=--------------------
===+++++++++******++**++++++++++++++++++++++++++***********+===+++=====+++++**+---------------------
===++++++++*******++*#*+++++++++++++++++++++++**************+==++++===+++++*####*-------------------
===+++++++++*****##*##**+++++++++++++++++++++*******+++++****++++*+++++++++###**=-------------------
===++++++++*****##*###****+++++++++++++++*********####*********+++++++++++***=+++-------------------
===+++++++**********##****++++++++++++++***####%%###########*****+++++++++**+++**-------------------
===+++++++********=**#****+++++++++++++***#%%@@@@%##*++**+*%%%#**+++++++++**==+---------------------
===+++++++*******###*##****+++++++++++*****#%@@@@@@@@@@@@@%%%#**++++++++++*+------------------------
===+++++++************#*****++++++++++***+++****###########**++++++++++++**+------------------------
===++++++++***********##*****++++++++++++++++***************+++++++++++++**=------------------------
===+++++++************####****+++++++++++++++**************+++++++++++++**+-------------------------
==++++++++***********######*****++++++++++++++*****##*****+++++++++++++**+--------------------------
==+++++++++***********###**#******+++++++++++++++******++++++=+++++++++*+---------------------------
==+++++++++**********####*+*##**********+++++++++++++++========+*++++***=---------------------------
=++++++++++**********####*++*#########**++++==================++*******=----------------------------
=++++++++++*********#####*++**#########**+++++==============+++****##*=-----------------------------
=+++++++++******########**+****#########****+++++++=====+++++**######*++=---------------------------
=++++++++**********#%###*++*****####%%%#####*****++++++++****######%@@%#***++=----------------------
+++++++******++++**%%%%@#+******###%%%%%%%#####***********####%%%##%%@%********+==------------------
++++++****+++++****%%@@@#+******####%%%%%%%%###############%%%%%#*#%%#************+=----------------
+++++**++++++******%%%@%*********#####%%%%%%%%%%%%%%%%#%%%%%%%#****%%***************+=--------------
+++++++++++********%@@%#*********######%%%%%%%%%%%%%%%%%%%%%%#****##**+***************+=---------===
-> It is Yasha <-
"""
