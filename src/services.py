import logging
import math
import os
from collections import defaultdict

from src.utils import open_excel_file, write_to_file

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path_cashback = os.path.join(project_root, "data", "cashback.json")


def category_cashback(year: str, month: str, data=open_excel_file()):
    """
    Функция принимает год, месяц и список транзакций, производит вычисление топ-3 категорий кэшбэка и передает словарь
    с категориями и путь записи конечного файла
    """
    category_logger = logging.getLogger("category_cashback")
    console_handler = logging.StreamHandler()
    category_logger.addHandler(console_handler)
    category_logger.setLevel(logging.INFO)
    category_logger.info("Начало работы функции category_cashback")
    data_list = data.to_dict(orient="records")
    result_year = []
    result_month = []

    category_logger.info("Производится поиск кэшбэка в транзакциях в указанный период")
    for operation in data_list:
        if year == str(operation.get("Дата платежа"))[-4:]:
            result_year.append(operation)

    if result_year:
        for transact in result_year:
            if month == str(transact.get("Дата платежа"))[-7:-5]:
                result_month.append(transact)
    else:
        category_logger.error("Данные по транзакциям отсутствуют")
        return "Данные по транзакциям в указанный год отсутствуют"

    if result_month:
        result = {}
        operations = defaultdict(list)
        for record in result_month:

            if record.get("Статус") != "FAILED":
                number = record.get("Категория")
                summ_oper = record.get("Кэшбэк")
                value = float("nan")
                if not math.isnan(summ_oper):
                    operations[number].append(summ_oper)
        for k, v in operations.items():
            summ = sum(v)
            result[k] = summ
        return write_to_file(result, path_cashback)
    else:
        category_logger.error("Данные по транзакциям отсутствуют")
        return "Данные по транзакциям в указанный месяц отсутствуют"
