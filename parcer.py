import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from ShopClasses.Wildberries import Wildberries
from ShopClasses.Ozon import  Ozon
from Driver import setup_driver


def main():
    query = "кружка с двойным дном"
    driver = setup_driver()

    try:
        wildberries = Wildberries(
            shop_name="Wildberries",
            driver=driver,
            shop_main_link="http://www.wildberries.ru/",
            encoding="utf-8",
        )

        wildberries.parse_search_page_without_filters(query=query)
        wildberries.apply_filters(price_from=400, price_to=1200, delivery_time="Любой")
        results = wildberries.parse_filtered_items(4.5) # если пользователь поставил пожелания по рейтингу, то надо передать рейтинг, например 4.7
        wildberries.save_result_to_html(results=results)

        print(f"Результаты сохранены в index_{wildberries.shop_name}.html")

    except Exception as e:
        print(f"Ошибка {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()