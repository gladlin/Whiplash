# Импорт необходимых библиотек для работы с HTTP-запросами, многопоточностью и типами данных
import requests
import time
import json
import hashlib
import threading
from queue import Queue
from typing import List, Dict, Optional


class WildberriesParser:
    def __init__(self,
                 min_price: Optional[float] = None,
                 max_price: Optional[float] = None,
                 min_rating: Optional[float] = None,
                 delivery_time: Optional[str] = None,
                 max_products: int = 50,
                 num_threads: int = 4):

        # URL для поиска товаров на Wildberries
        self.search_url = "https://search.wb.ru/exactmatch/ru/common/v4/search"
        # Заголовки для HTTP-запросов, требования к браузеру, который открываем,
        # на котором мы и будем отправлять разные запросы к бд вб
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        # Список для хранения информации о товарах
        self.products = []
        # Блокировка для синхронизации доступа к списку товаров
        self.products_lock = threading.Lock()
        # Параметры фильтрации
        self.min_price = min_price
        self.max_price = max_price
        self.min_rating = min_rating
        self.delivery_time = delivery_time
        self.max_products = max_products
        self.num_threads = num_threads

    def _generate_unique_params(self, query, page=1):
        """Генерация уникальных параметров для запроса"""
        # Текущее время в миллисекундах
        timestamp = int(time.time() * 1000)

        # Создаем уникальный идентификатор на основе запроса и времени
        unique_id = hashlib.md5(f"{query}{timestamp}".encode()).hexdigest()

        # Базовые параметры для запроса
        params = {
            'appType': 1,
            'curr': 'rub',
            'dest': '-1257786',  # Стандартный параметр для региона
            'query': query,
            'resultset': 'catalog',
            'page': page,
            'suppressSpellCheck': 'false',
            'timestamp': timestamp,
            'unique_id': unique_id
        }

        # Добавляем фильтр по цене (в копейках)
        if self.min_price is not None or self.max_price is not None:
            min_price_kopecks = int((self.min_price or 0) * 100)
            max_price_kopecks = int((self.max_price or 1000000) * 100)
            params['priceU'] = f'{min_price_kopecks};{max_price_kopecks}'

        # Добавляем фильтр по доставке
        delivery_map = {
            'послезавтра': 70,
            'завтра': 46,
            'до 3 дней': 94,
            'до 5 дней': 142
        }
        if self.delivery_time and self.delivery_time in delivery_map:
            params['fdlvr'] = delivery_map[self.delivery_time]

        # Добавляем фильтр по рейтингу (если указан)
        if self.min_rating is not None:
            params['frating'] = 1

        return params

    def _get_basket_host(self, product_id):
        """Определение номера хоста basket на основе ID товара"""
        # Преобразуем ID товара в число
        nm = int(product_id)
        vol = nm // 100000  # Эквивалент ~~(nm / 1e5)

        # Логика определения хоста
        if 0 <= vol <= 143:
            host = '01'
        elif 144 <= vol <= 287:
            host = '02'
        elif 288 <= vol <= 431:
            host = '03'
        elif 432 <= vol <= 719:
            host = '04'
        elif 720 <= vol <= 1007:
            host = '05'
        elif 1008 <= vol <= 1061:
            host = '06'
        elif 1062 <= vol <= 1115:
            host = '07'
        elif 1116 <= vol <= 1169:
            host = '08'
        elif 1170 <= vol <= 1313:
            host = '09'
        elif 1314 <= vol <= 1601:
            host = '10'
        elif 1602 <= vol <= 1655:
            host = '11'
        elif 1656 <= vol <= 1919:
            host = '12'
        elif 1920 <= vol <= 2045:
            host = '13'
        elif 1920 <= vol <= 2189:
            host = '14'
        elif 1920 <= vol <= 2405:
            host = '15'
        elif 1920 <= vol <= 2621:
            host = '16'
        elif 1920 <= vol <= 2837:
            host = '17'
        else:
            host = '18'

        return host

    def _get_product_details(self, product_url: str, num_of_pictures: int) -> Dict[str, list]:
        """Получение деталей товара с использованием безопасного подхода"""
        try:
            # Извлекаем ID товара из URL
            product_id = product_url.split('/')[-2]
            host = self._get_basket_host(product_id)

            # Формируем URL для получения данных о товаре
            description_url = f"https://basket-{host}.wbbasket.ru/vol{int(product_id) // 100000}/part{int(product_id) // 1000}/{product_id}/info/ru/card.json"

            # Выполняем GET-запрос для получения информации о товаре
            response = requests.get(description_url, headers=self.headers, timeout=3)
            response.raise_for_status()

            # Извлекаем описание товара из ответа
            description_data = response.json()
            description_text = description_data.get('description', '')
            images = []
            for i in range(1, num_of_pictures + 1):
                image_url = f"https://basket-{host}.wbbasket.ru/vol{int(product_id) // 100000}/part{int(product_id) // 1000}/{product_id}/images/big/{i}.webp"
                images.append(image_url)

            return {
                'Полное описание': description_text,
                'Изображение': images
            }

        except Exception as e:
            print(f"Ошибка при получении деталей: {e}")
            return {'description': '', 'images': []}

    def search_products(self, query: str, page: int = 1) -> List[Dict]:
        """Поиск товаров с многопоточной обработкой"""
        # Генерируем параметры запроса
        params = self._generate_unique_params(query, page)

        try:
            # Выполняем запрос к API поиска товаров
            response = requests.get(self.search_url, params=params, headers=self.headers)
            response.raise_for_status()

            # Извлекаем список товаров из ответа
            data = response.json()
            products = data.get('data', {}).get('products', [])

            # Ограничиваем количество товаров
            products = products[:self.max_products]

            # Создаем очереди для товаров и результатов
            product_queue = Queue()
            result_queue = Queue()

            # Заполняем очередь товаров
            for product in products:
                product_queue.put(product)

            # Создаем и запускаем потоки для обработки товаров
            threads = []
            for _ in range(self.num_threads):
                thread = threading.Thread(target=self._worker, args=(product_queue, result_queue))
                thread.start()
                threads.append(thread)

            # Ждем завершения всех потоков
            product_queue.join()

            # Собираем результаты обработки
            processed_products = []
            while not result_queue.empty():
                processed_products.append(result_queue.get())

            # Сохраняем результаты в файл
            with open('wildberries_product_list.json', 'w', encoding='utf-8') as f:
                json.dump(processed_products, f, ensure_ascii=False, indent=4)

            return processed_products

        except Exception as e:
            print(f"Ошибка при поиске: {e}")
            return []

    def _worker(self, product_queue: Queue, result_queue: Queue):
        """Поток для обработки товаров"""
        while not product_queue.empty():
            try:
                # Извлекаем товар из очереди
                product = product_queue.get(block=False)

                # Формируем URL товара
                product_url = f"https://www.wildberries.ru/catalog/{product.get('id', '')}/detail.aspx"
                # Получаем детали товара
                details = self._get_product_details(product_url, product.get('pics', 0))

                # Формируем обработанную информацию о товаре
                processed_product = {
                    'Название': product.get('name', ''),
                    'Цена': product.get('salePriceU', 0) / 100,
                    'Рейтинг': product.get('reviewRating', 0),
                    'Ссылка': product_url,
                    **details
                }

                # Помещаем обработанный товар в очередь результатов
                result_queue.put(processed_product)
            except Exception as e:
                print(f"Ошибка в потоке: {e}")
            finally:
                # Отмечаем задачу как выполненную
                product_queue.task_done()

# Пример использования
if __name__ == "__main__":
    # Пример с фильтрацией по цене, рейтингу и доставке
    parser = WildberriesParser(
        min_price=300,
        max_price=700,
        min_rating=4,
    )
    products = parser.search_products("фурри")
    print("Парс завершен успешно")

"""
------------------------
───▐▀▄──────▄▀▌───▄▄▄▄▄▄▄
───▌▒▒▀▄▄▄▄▀▒▒▐▄▀▀▒██▒██▒▀▀▄
──▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀▄
──▌▒▒▒▒▒▒▒▒▒▒▒▒▒▄▒▒▒▒▒▒▒▒▒▒▒▒▒▀▄
▀█▒▒█▌▒▒█▒▒▐█▒▒▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▌
▀▌▒▒▒▒▒▀▒▀▒▒▒▒▒▀▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▐ ▄▄        это должен был быть котик :о
▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▄█▒█
▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▀
──▐▄▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▄▌
────▀▄▄▀▀▀▀▄▄▀▀▀▀▀▀▄▄▀▀▀▀▀▀▄▄▀
"""

