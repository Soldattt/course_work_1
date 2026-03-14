import re
from datetime import datetime
from typing import Any

from src.reports import spending_by_category
from src.services import category_cashback
from src.views import views


def main() -> Any:
    date_obj = datetime.now()
    valid_year = False
    valid_month = False
    valid_category = False
    while not valid_year:
        year = input("Введите год проведения анализа (Пример 2025):\n")
        year_pattern = re.compile(r'\d{4}')
        if year_pattern.fullmatch(year):
            valid_year = True
            while not valid_month:
                month_pattern = re.compile(r'\d{2}')
                month = input("Введите месяц проведения анализа цифрами(Пример 03):\n")
                if month_pattern.fullmatch(month):
                    valid_month = True
                    date = input("Введите дату для подсчета трат за последние 3 месяца в формате ДД.ММ.ГГГГ "
                                 "или пропустите ввод для выбора текущей даты:\n")
                    while not valid_category:
                        spending_category = input("Введите категорию для подсчета трат:\n")
                        if spending_category:
                            valid_category = True

                        return (views(date_obj), category_cashback(year, month),
                                spending_by_category(spending_category, date))


if __name__ == "__main__":
    print(main())
