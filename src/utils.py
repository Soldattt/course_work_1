import json
import logging
import os
import time
from collections import defaultdict
from heapq import nsmallest
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY_AMOUNT = os.getenv("API_KEY_AMOUNT")
URL_AMOUNT = os.getenv("URL_AMOUNT")
API_KEY_STOCK = os.getenv("API_KEY_STOCK")
URL_STOCK_1 = os.getenv("URL_STOCK_1")
URL_STOCK_2 = os.getenv("URL_STOCK_2")

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path_excel = os.path.join(project_root, "data", "operations.xlsx")


def open_excel_file(path: str = path_excel) -> Any:
    """
    Функция считывает финансовые операции из файла .xlsx по указываемому пути и выдает список словарей с транзакциями
    """
    file_logger = logging.getLogger("open_excel_file")
    console_handler = logging.StreamHandler()
    file_logger.addHandler(console_handler)
    file_logger.setLevel(logging.INFO)
    file_logger.info("Начало работы функции open_excel_file")
    try:
        file_logger.info("Считывание данных из файла")
        excel_reader = pd.read_excel(path)
        return excel_reader
    except FileNotFoundError:
        file_logger.critical("Файл отсутствует")
        return "Файл не найден"


def data_for_json(greeting: str, data: Any = open_excel_file()) -> Any:
    """
    Функция принимает на вход приветствие и список транзакций и производит выборку необходимых данных
    в соответствии с ТЗ, затем передает словарь с данными для записи в json файл
    """
    data_logger = logging.getLogger("data_for_json")
    console_handler = logging.StreamHandler()
    data_logger.addHandler(console_handler)
    data_logger.setLevel(logging.INFO)
    data_logger.info("Начало работы функции data_for_json")

    data = data.to_dict(orient="records")
    result = []
    result_dict = {}
    operations = []
    card_operations = defaultdict(list)
    data_logger.info("Производится отсеивание неуспешных транзакций и определение топ-5 транзакций")
    for record in data:
        if record.get("Статус") != "FAILED":
            number = record.get("Номер карты")
            summ = record.get("Сумма платежа")

            if isinstance(number, str) and int(summ) < 0:
                operations.append(record)
                card_operations[number].append(summ)
                counted = nsmallest(5, operations, key=lambda item: item["Сумма операции"])
    counted_list = counted

    for k, v in card_operations.items():
        summ = sum(v)
        cards = {}
        cards["last_digits"] = k[1:]
        cards["total_spent"] = abs(summ)
        cards["cashback"] = abs(round(summ / 100, 2))
        result.append(cards)
        result_dict["greeting"] = greeting
        result_dict["cards"] = result

    top_transactions = []

    for item in counted_list:
        transactions = {}
        top_transactions.append(transactions)
        for k, v in item.items():
            if k == "Дата платежа":
                transactions["date"] = v
        for k, v in item.items():
            if k == "Сумма операции с округлением":
                transactions["amount"] = v
        for k, v in item.items():
            if k == "Категория":
                transactions["category"] = v
        for k, v in item.items():
            if k == "Описание":
                transactions["description"] = v

    result_dict["top_transactions"] = top_transactions

    data_logger.info("Производится получение актуальных курсов валют")

    currency_rates = []
    cur_eur = {}
    cur_usd = {}

    response_eur = requests.get(f"{URL_AMOUNT}{API_KEY_AMOUNT}/pair/EUR/RUB")
    response_usd = requests.get(f"{URL_AMOUNT}{API_KEY_AMOUNT}/pair/USD/RUB")
    data_eur = response_eur.json()
    data_usd = response_usd.json()

    eur_rate = round(float(data_eur.get("conversion_rate")), 2)
    usd_rate = round(float(data_usd.get("conversion_rate")), 2)

    cur_eur["currency"] = "EUR"
    cur_eur["rate"] = eur_rate
    cur_usd["currency"] = "USD"
    cur_usd["rate"] = usd_rate
    currency_rates.append(cur_eur)
    currency_rates.append(cur_usd)
    result_dict["currency_rates"] = currency_rates
    stock_prices = []
    data_logger.info("Производится получение стоимости топовых акций S&P500")

    stocks_nvda = {}
    stocks_appl = {}
    stocks_amzn = {}
    stocks_msft = {}
    stocks_googl = {}
    response_nvda = requests.get(f"{URL_STOCK_1}NVDA{URL_STOCK_2}{API_KEY_STOCK}")
    data_nvda = response_nvda.json()
    stocks_nvda["stock"] = "NVDA"
    stocks_nvda["price"] = data_nvda.get("Global Quote").get("05. price")
    stock_prices.append(stocks_nvda)

    time.sleep(3)
    response_aapl = requests.get(f"{URL_STOCK_1}AAPL{URL_STOCK_2}{API_KEY_STOCK}")
    data_aapl = response_aapl.json()
    stocks_appl["stock"] = "AAPL"
    stocks_appl["price"] = data_aapl.get("Global Quote").get("05. price")
    stock_prices.append(stocks_appl)

    time.sleep(3)
    response_amzn = requests.get(f"{URL_STOCK_1}AMZN{URL_STOCK_2}{API_KEY_STOCK}")
    data_amzn = response_amzn.json()
    stocks_amzn["stock"] = "AMZN"
    stocks_amzn["price"] = data_amzn.get("Global Quote").get("05. price")
    stock_prices.append(stocks_amzn)

    time.sleep(3)
    response_msft = requests.get(f"{URL_STOCK_1}MSFT{URL_STOCK_2}{API_KEY_STOCK}")
    data_msft = response_msft.json()
    stocks_msft["stock"] = "MSFT"
    stocks_msft["price"] = data_msft.get("Global Quote").get("05. price")
    stock_prices.append(stocks_msft)

    time.sleep(3)
    response_googl = requests.get(f"{URL_STOCK_1}GOOGL{URL_STOCK_2}{API_KEY_STOCK}")
    data_googl = response_googl.json()
    stocks_googl["stock"] = "GOOGL"
    stocks_googl["price"] = data_googl.get("Global Quote").get("05. price")
    stock_prices.append(stocks_googl)

    result_dict["stock_prices"] = stock_prices
    return result_dict


def write_to_file(result_dict: dict, path: str) -> Any:
    """
    Функция принимает на вход словарь с данными по транзакциям, путь файла и производит запись
    данных в этот файл
    """
    json_logger = logging.getLogger("write_to_file")
    console_handler = logging.StreamHandler()
    json_logger.addHandler(console_handler)
    json_logger.setLevel(logging.INFO)
    json_logger.info("Начало работы функции write_to_file")

    json_logger.info("Производится запись данных в файл")
    with open(f"{path}", "w", encoding="utf-8") as f:
        json.dump(result_dict, f, ensure_ascii=False)
        return "Данные записаны в Ваш файл"
