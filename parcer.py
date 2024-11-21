import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled") #флаг чтобы не банилол что типо бот пришел на сайт
    driver = uc.Chrome(options=options)
    return driver


def search_wildberries(driver, query):
    driver.get("https://www.wildberries.ru/")
    print("Открыт сайт Wildberries.") #всякие такие принты нужны просто чтобы отследить на каком этапе и могло застопориться

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "searchInput"))
    )
    print("Поисковая строка найдена. Вводим запрос...")

    search_box = driver.find_element(By.ID, "searchInput")
    search_box.click() #имитация действий пользователя, что когда он хочет ввести что-то в поиск, то он должен нажать на него
    search_box.send_keys(query)
    search_box.send_keys(Keys.ENTER)#типо нажимаем кнопку ентер

    print("Запрос отправлен. Ожидаем загрузки результатов...")
    WebDriverWait(driver, 60).until(
        lambda d: d.execute_script("return document.querySelectorAll('.product-card__wrapper').length > 0")
    )
    print("Результаты поиска загрузились.")

    with open("page_debug.html", "w", encoding="utf-8") as f: #файл, в котором прям вся страница с поиском ноута, городом новосибом родненьким и еще чем-то может быть
        f.write(driver.page_source)
    print("HTML текущей страницы сохранён в 'page_debug.html'.")



def parse_results(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    items = soup.select("div.product-card__wrapper")

    results = []
    for item in items:
        try:
            title_tag = item.select_one("span.product-card__name") #тег с названием товара
            title = title_tag.text.strip() if title_tag else "Название отсутствует"

            price_tag = item.select_one("ins.price__lower-price") #тег содержанием цены товара(окончательной)
            price = price_tag.text.strip() if price_tag else "Цена отсутствует"

            rating_tag = item.select_one("span.address-rate-mini") #просто общий рейтинг товара в звездах
            rating = rating_tag.text.strip() if rating_tag else "Рейтинг отсутствует"

            link_tag = item.select_one("a") #ссылка на саму карточку товара
            link = f"https://www.wildberries.ru/{link_tag['href']}" if link_tag else "Ссылка отсутствует"

            results.append({
                "Название": title,
                "Цена": price,
                "Рейтинг": rating,
                "Ссылка": link,
            })
        except Exception as e:
            print(f"Ошибка при обработке товара: {e}")
            continue

    return results


def save_results_to_html(results, filename="index.html"): #формируется файл с табличкой с наименованием, ссылкой и ценой на товары из одной страницы
    html_content = """
    <html>
    <head><title>Результаты поиска</title></head>
    <body>
    <h1>Результаты поиска</h1>
    <table border="1">
        <tr>
            <th>Название</th>
            <th>Цена</th>
            <th>Ссылка</th>
        </tr>
    """
    for result in results:
        html_content += f"""
        <tr>
            <td>{result['Название']}</td>
            <td>{result['Цена']}</td>
            <td><a href="{result['Ссылка']}">Ссылка</a></td>
        </tr>
        """
    html_content += """
    </table>
    </body>
    </html>
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)


def main():
    query = "ноутбук" #потом надо добавить с проставлением цены и критерий отзывов, но сейчас хотя бы так работает - уже победа!
    driver = setup_driver()
    #вообще код выполняется примерно секунд за 30 примерно(смэрть), но может быть можно будет уменьши время ожидания от сайтика и тогда будет итоговое время меньше
    #но скажу често, что не было сил проверять, да и лень уже было как-то, а я пошла пить чай
    try:
        search_wildberries(driver, query)
        results = parse_results(driver)
        save_results_to_html(results)
        print("Результаты сохранены в index.html")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

"""⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣀⠈⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠿⢿⣿⣿⣿⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠠⣿⠟⠛⠛⠃⠁⢹⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠙⠀⠀⠀⠀⠀⡿⢋⣼⣿⣿⠟⣡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⢠⣤⣤⣄⠀⣡⣿⣿⠟⣡⣾⣿⣿⣿⣿⣿⣿⡘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⢈⣿⣿⠁⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿
⠀⣴⣿⣿⡇⣰⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠁⢠⣿⣿⣆⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢀⣿⣿⣿
⠀⢻⣿⣿⡀⠻⠿⠿⠿⠿⠛⠛⠁⠀⠀⠀⢀⣼⣿⣿⣿⡀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⣼⣿⣿⣿
⣷⡄⠙⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⣿⣿⣿⣷⡄⠀⠉⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣼⣿⣿⣿⡿
⣿⣿⣆⢀⣧⠀⠀⠀⢀⣀⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠈⠙⠛⠟⠛⠛⠛⠛⠛⠛⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⣴⣿⣿⡿⠋⢀
⣿⣿⣿⣿⣿⣧⣄⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⢄⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢁⣼⣿⠟⠁⢀⣴⣿
⣿⣿⣿⣿⣿⣿⣿⣾⡀⠘⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠻⣿⣿⣿⣿⣿⣷⣦⣤⣄⣀⠀⠀⠀⠀⠀⠈⠻⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⢠⡿⠋⠀⣠⣴⣿⣿⣿
⢿⣿⣿⣿⣿⣿⣿⠿⠿⠓⢀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⡀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠐⠋⠀⣠⣾⣿⣿⣿⣿⣿
⣸⣿⣿⣯⡿⠏⠁⠀⠀⠀⠀⠀⠀⠈⠀⣀⣀⠈⠉⠻⡿⣿⣿⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀⠈⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿
⢸⣿⡟⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣯⡀⠀⠀⠀⠀⢻⣿⠈⣿⣿⣿⣿⡿⠿⠛⠛⠛⠿⣛⣿⣿⣿⣿⣿⣿⣿⣷⡄⢹⣿⣿⣿⣿⡏⢀⣠⣤⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡏⠀⠀⠐⠛⠀⢸⡇⣠⣿⣿⡿⠏⢀⣠⣤⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⣠⠾⢛⠁⠀⠀⢛⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣄⠙⠧⡀⠂⠀⠀⠀⣾⣧⣿⣿⡟⠁⢀⣾⣿⠇⠀⠀⣀⠀⠀⠀⠀⠹⢻⣿⣿⣿⣿⣿⣿⠋⢠⣶⠏⠰⠁⠀⠀⠀⠀⠘⠿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡿⠶⠤⠄⠀⠀⣰⣿⡋⣿⣿⣧⠀⢸⣿⣿⠀⠀⠘⠟⠀⠀⢸⡄⠀⣸⣿⣿⣿⣿⣿⠃⢀⡜⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣶⣶⣾⣿⣿⠋⣼⣿⣿⣿⣇⠈⢻⣿⡄⠠⣄⡀⠄⢀⣾⠟⢀⣿⣿⣿⣿⣿⠃⣠⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⢻⣿⣿
⠀⠀⠀⠢⡀⠀⠀⠀⠀⠀⠀⠤⠀⣿⣿⣿⣿⣿⣿⡿⠃⣼⣿⣿⣿⡅⢿⠇⢢⣈⡉⠒⠀⠀⠀⣩⣤⣶⣾⣿⣿⣿⣿⠷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛
⠀⠀⠀⠀⠀⠑⠤⣀⠉⠳⠤⣤⠀⢹⣿⣷⣿⣿⡟⠀⣜⣿⣿⣿⣿⣿⣿⣷⣄⣈⣉⣛⣛⣛⣋⣡⣼⣿⣿⣿⣿⣟⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠉⠂⠀⠀⠀⢸⣿⣿⣿⡟⢀⣾⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣛⣛⣻⣿⣿⠋⠠⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠐⣶⣶⡄⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣹⡏⠀⠀⢰⠁⠐⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠸⢿⣿⠃⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣽⡟⠐⣷⣄⡁⣸⣿⣿⣾⠂⠀⠠⠀⢰⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣰⡿⠀⠀⢦⠈⠻⣿⣿⣿⣿⣷⣄⡀⠀⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⢁⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠿⢿⣿⣿⣿⣿⣿⡓⣶⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⣩⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠋⠙⠛⠻⢿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢷⣮⣽⣿⣿⣿⣿⠟⢋⣤⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠙⠿⠛⣿⣋⣀⠘⠻⠿⠿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠂⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡃⠈⠻⠿⡿⠿⣿⣿⣿⣶⣤⡉⠻⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀⢀⣸⣦⣤⣤⣉⣙⣛⣿⣆⡙⠏⢿⣿⠋⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                no bitches?⠀⠀⠀⠀⠀⠀
"""