import requests
from bs4 import BeautifulSoup

import Driver
import time
from pprint import pprint

url = "https://photos.okolo.app/product/1166157-main/320x320.jpeg?updated_at=2024-11-22T12:27:38.951Z"
#
# head_accept = r"text\html"
# head_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
# head_accept_language = "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
# header_content_type = "text/html;charset=utf-8"
#
# header = {
#     "Accept": head_accept,
#     "User-Agent": head_user_agent,
#     "Accept-Language": head_accept_language,
#     "Content-Type": header_content_type
# }
#
# page = requests.get(url = url, headers = header)
# soup = BeautifulSoup(page.text, "html.parser")

driver = Driver.setup_driver()

driver.get(url)

time.sleep(5)

driver.save_screenshot("Abobus_sucksus.png")

pprint(driver.options.arguments)

# print(soup.prettify())
