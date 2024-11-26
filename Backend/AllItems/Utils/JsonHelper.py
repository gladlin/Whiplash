import json
from json import dumps, loads
from copy import deepcopy
import os
from pprint import pprint

# Преобразование из объекта 'dict' в строку JSON.
def convert_from_dict_to_json_string( just_dict: dict ) -> str:
    try:
        return str( dumps(just_dict, ensure_ascii = False) )
    except Exception as e:
        print(e)
    return None

# Преобразование из обычного объекта 'dict' в JSON версию 'dict'.
def convert_from_dict_to_json_dict(just_dict: dict) -> dict:
    try:
        return dict( loads( dumps( just_dict, ensure_ascii = False ) ) )
    except Exception as e:
        print(e)
    return None

# Преобразование из объекта 'list' в строку JSON.
def convert_from_json_string_to_dict( json_string: str ) -> dict:
    try:
        return dict( loads(json_string) )
    except Exception as e:
        print(e)
    return None

# Преобразование из строки JSON в объект 'dict'.
def convert_from_list_to_json_string( just_list: list ) -> str:
    try:
        return str( dumps(just_list, ensure_ascii = False) )
    except Exception as e:
        print(e)
    return None

# Преобразование из строки JSON в объект 'list'.
def convert_from_json_string_to_list( json_string: str ) -> list:
    try:
        return list( loads(json_string) )
    except Exception as e:
        print(e)
    return None

# Преобразование из обычного объекта 'list' в JSON версию 'list'.
def convert_from_list_to_json_list(just_list: list) -> list:
    try:
        return list( loads( dumps( just_list, ensure_ascii = False ) ) )
    except Exception as e:
        print(e)
    return None

# Запись информации из объекта 'dict' с проверкой достоверности записанной информации.
def write_dict_to_json_file(
        just_dict: dict,
        filename_without_extends: str = "write_dict_to_json_file",
        encoding = "utf-8"
) -> bool:
    _dict = deepcopy(just_dict)

    filename = filename_without_extends + ".json"
    abs_path = os.path.abspath(os.curdir) + f"\\{filename}"

    try:

        # Creating JSON file.
        with open(filename, "w", encoding = encoding) as writable_file:
            writable_file.write(dumps(_dict, indent=4, ensure_ascii = False))
            writable_file.close()
        # Reading JSON file for checking.
        read_json_dict: dict = read_json_file_and_return_dict(filename, encoding)

        _dict_for_compare = dict( loads(dumps(_dict, ensure_ascii = False)) )

        # If JSON file was created and created file's information equals dumped information in '_dict'.
        return os.path.exists( abs_path ) and are_dicts_equals(read_json_dict, _dict_for_compare)
    except Exception as e:
        print(e)
    return False

# Запись информации из объекта 'list' с проверкой достоверности записанной информации.
def write_list_to_json_file(
        just_list: list,
        filename_without_extends: str = "write_list_to_json_file",
        encoding: str = "utf-8"
) -> bool:
    _list = deepcopy(just_list)

    filename = filename_without_extends + ".json"
    abs_path = os.path.abspath(os.curdir) + f"\\{filename}"

    try:
        # Creating JSON file.
        with open(filename, "w", encoding = encoding) as writable_file:
            writable_file.write(dumps(_list, indent=4, ensure_ascii = False))
            writable_file.close()
        # Reading JSON file for checking.
        read_json_list: list = read_json_file_and_return_list(filename, encoding)

        _list_for_compare = list( loads(dumps(_list, ensure_ascii = False)) )

        # If JSON file was created and created file's information equals dumped information in '_dict'.
        return os.path.exists( abs_path ) and are_lists_equals(read_json_list, _list_for_compare)
    except Exception as e:
        print(e)
    return False

# Чтение файла JSON с преобразованием в объект 'dict'.
def read_json_file_and_return_dict(filename_with_extends: str, encoding = "utf-8") -> dict:
    result: dict = dict()

    try:
        with open(filename_with_extends, "r", encoding = encoding) as readable_file:
            result: dict = dict( loads(readable_file.read()) )
            readable_file.close()
    except Exception as e:
        print(e)
    return result

# Чтение файла JSON с преобразованием в объект 'list'.
def read_json_file_and_return_list(filename_with_extends: str, encoding = "utf-8") -> list:
    result: list = list()

    try:
        with open(filename_with_extends, "r", encoding = encoding) as readable_file:
            result: list = list( loads(readable_file.read()) )
            readable_file.close()
    except Exception as e:
        print(e)
    return result

# Сравнение двух объектов типа 'dict'.
def are_dicts_equals(dict1: dict, dict2: dict) -> bool:
    try:
        return dict1.__eq__(dict2)
    except Exception as e:
        print(e)
    return None

# Сравнение двух объектов типа 'list'.
def are_lists_equals(list1: list, list2: list) -> bool:
    try:
        return list1.__eq__(list2)
    except Exception as e:
        print(e)
    return None


listt = [
    {
        "id": 0,
        "Название": "Mortis",
        "Цена": "200"
    },
    {
        "id": 1,
        "Название": "El-Primo",
        "Цена": "500"
    }
]

dictt = {
    "id": 3,
    "Название": "Poco",
    "Цена": "250"
}

"""
listt_string = convert_from_list_to_json_string( listt )
dictt_string = convert_from_dict_to_json_string( dictt )
print()
pprint( listt )
pprint( dictt )
print()
pprint( listt_string )
pprint( dictt_string )
print()
pprint( convert_from_json_string_to_list( listt_string ) )
pprint( convert_from_json_string_to_dict( dictt_string ) )
print()
pprint( write_list_to_json_file( listt ) )
pprint( write_dict_to_json_file( dictt ) )
print()
pprint( convert_from_list_to_json_list( listt ) )
pprint( convert_from_dict_to_json_dict( dictt ) )
"""
