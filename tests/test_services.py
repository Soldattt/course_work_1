import os

from src.services import category_cashback
from src.utils import open_excel_file

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
test_path_excel = os.path.join(project_root, "tests", "test_data", "test_operations.xlsx")
path_cashback = os.path.join(project_root, "tests", "test_data", "test_cashback.json")


def test_services_year():
    result = category_cashback("2025", "02", open_excel_file(test_path_excel))
    assert result == "Данные по транзакциям в указанный год отсутствуют"


def test_services_month():
    result = category_cashback("2021", "02", open_excel_file(test_path_excel))
    assert result == "Данные по транзакциям в указанный месяц отсутствуют"


def test_services():
    result = category_cashback("2021", "12", open_excel_file(test_path_excel))
    assert result == "Данные записаны в Ваш файл"
