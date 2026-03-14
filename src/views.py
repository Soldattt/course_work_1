import logging
import os

from src.utils import data_for_json

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path_operations = os.path.join(project_root, "data", "operations.json")


def views(date_obj):
    """
    Функция принимает на вход дату, производит определение времени суток и передает приветствие и
    путь записи конечного файла
    """
    views_logger = logging.getLogger("views")
    console_handler = logging.StreamHandler()
    views_logger.addHandler(console_handler)
    views_logger.setLevel(logging.INFO)
    views_logger.info("Начало работы функции views_logger")
    now = int(date_obj.strftime("%H"))

    if 0 <= now < 6 and now == 23:
        greeting = "Доброй ночи"
    elif 6 <= now < 12:
        greeting = "Доброе утро"
    elif 12 <= now < 16:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"
    return data_for_json(greeting, path_operations)
