import datetime
import logging
import os
from datetime import datetime
from typing import Any

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.utils import open_excel_file

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path_spending = os.path.join(project_root, "data", "spending.json")
pd.set_option("display.max_columns", None)


def spending_by_category(spending_category: str, date: str = None, data: Any = open_excel_file()) -> Any:
    category_logger = logging.getLogger("spending_by_category")
    console_handler = logging.StreamHandler()
    category_logger.addHandler(console_handler)
    category_logger.setLevel(logging.INFO)
    category_logger.info("Начало работы функции spending_by_category")
    """
    Функция принимает дату, наименование категории и DataFrame с транзакциями, производит сортировку
    по дате(последние три месяца от указанной даты) и категории и возвращает отсортированный DataFrame
    """
    df = data.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    if date is None:
        category_logger.info("Получение текущей даты, т.к. дата не была указана")
        date = datetime.now()
    else:
        category_logger.info("Сортировка по дате и категории")
        date = datetime.strptime(date, r"%d.%m.%Y")
    start_date = date - relativedelta(months=3)
    filtered_df = df[
        (df["Дата операции"] >= start_date) & (df["Дата операции"] <= date) & (df["Категория"] == spending_category)
    ]
    if filtered_df.to_dict().get("Дата операции") == {}:
        category_logger.error("Данных не обнаружено")
        return "Транзакций по введенным данным не обнаружено"
    else:
        category_logger.info("Вывод данных")
        return filtered_df
