import time
from pprint import pprint

import JsonHelper
from ShopClasses.Pyatyourochka import Pyatyourochka
from ShopClasses.Wildberries import Wildberries
from ShopClasses.Ozon import  Ozon
from Driver import setup_driver


def main():
    query = "Сметана"  # Потом надо добавить с проставлением цены и критерий отзывов, но сейчас хотя бы так работает - уже победа!
    driver = setup_driver()
    #вообще код выполняется примерно секунд за 30 примерно(смэрть), но может быть можно будет уменьшить время ожидания от сайтика и тогда будет итоговое время меньше
    #но скажу честно, не было сил проверять, да и лень уже было как-то, а я пошла пить чай.

    # DER-2SH-KA: приятного прошедшего чаепития.

    try:
        # # Wildberries.
        # print("\n*** Начало парсинга Wildberries ***\n")
        # wildberries = Wildberries(
        #     shop_name = "Wildberries",
        #     driver = driver,
        #     shop_main_link = "https://www.wildberries.ru/",
        #     encoding = "utf-8"
        # )
        #
        # wildberries.parse_search_page_without_filters(query = query)
        # wildberries.apply_filters(
        #     price_from=300,
        #     price_to=1000,
        #     delivery_time="Любой"
        # )
        # results_wb = (
        #     wildberries.cherrypick_of_parsed_search_page_without_filters()
        # )
        # # results_wb = wildberries.parse_filtered_items(4.5)
        # try:
        #     JsonHelper.write_list_to_json_file(
        #         results_wb,
        #         "wildberries_gde_posilka"
        #     )
        # except Exception as e1:
        #     print(e1)
        # wildberries.save_result_to_html(results = results_wb)
        # print(f"*** Результаты были сохранены в index_{wildberries.shop_name}.html ***")
        # # wildberries.driver_close()
        #
        # print("\n*** Конец парсинга Wildberries ***\n")
        #
        # # driver.__del__()
        # driver = setup_driver()


        # # Ozon.
        # ozon = Ozon(
        #     shop_name = "Ozon",
        #     driver = driver,
        #     shop_main_link = "https://www.ozon.ru/?__rr=1&abt_att=1",
        #     encoding = "utf-8"
        # )
        #
        # ozon.parse_search_page_without_filters(query = query)
        #
        # ozon.driver_close()

        print("\n*** Начало парсинга Пятёрочки ***\n")

        pyatyourochka = Pyatyourochka(
            shop_name = "Пятёрочка",
            driver = driver,
            shop_main_link = "https://5ka.ru",
            encoding = "utf-8"
        )
        pyatyourochka.parse_search_page_without_filters(query = query)
        results_pyatyourochka = (
            pyatyourochka.cherrypick_of_parsed_search_page_without_filters()
        )
        pprint(results_pyatyourochka)
        try:
            is_writen = JsonHelper.write_list_to_json_file(
                results_pyatyourochka,
                "Pyatorochka_Chingis"
            )

            if is_writen:
                print("JSON записан")
            else:
                print("JSON не записан")
        except Exception as e1:
            print(e1)
        # pprint(results_pyatyourochka)
        pyatyourochka.save_result_to_html(results = results_pyatyourochka)
        # pyatyourochka.driver_close()

        print("\n*** Конец парсинга Пятёрочки ***\n")

    except Exception as e:
        print(f"*** Ошибка {e} ***")
    finally:
        if driver:
            driver.quit()
    print("А я собака сутулая -- сбк'ен")


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