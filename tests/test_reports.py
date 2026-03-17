import os

from src.reports import spending_by_category
from src.utils import open_excel_file

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
test_path_excel = os.path.join(project_root, "tests", "test_data", "test_operations.xlsx")


def test_transaction_none():
    result = spending_by_category("Другое", "02.02.2020", open_excel_file(test_path_excel))
    assert result == "Транзакций по введенным данным не обнаружено"


def test_date_none():
    result = spending_by_category("Другое", None, open_excel_file(test_path_excel))
    assert result == "Транзакций по введенным данным не обнаружено"
