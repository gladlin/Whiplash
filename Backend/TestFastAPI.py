import requests as rq
from pprint import pprint
import os
from AllItems.Utils import JsonHelper

url = "http://127.0.0.1:8000/"

json_content = JsonHelper.read_json_file_and_return_list(
    os.getcwd() + "/AllItems/Utils/wildberries_product_list.json"
)

# content = rq.get(url=url)
# pprint(content.content)
pprint(json_content)