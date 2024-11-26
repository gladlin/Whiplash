import undetected_chromedriver as uc

def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-web-security")
    options.add_argument("--user-data-dir")
    options.add_argument("--disable-blink-features=AutomationControlled") # Флаг для обхода блокировки против ботов.
    driver = uc.Chrome(options=options)
    return driver