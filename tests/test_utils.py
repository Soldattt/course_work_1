import os

from src.utils import open_excel_file, write_to_file

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
test_path_excel = os.path.join(project_root, "tests", "test_data", "test_operations.xlsx")
test_path_excel_none = os.path.join(project_root, "tests", "test_data", "test_operations_none.xlsx")
path_operations_test = os.path.join(project_root, "tests", "test_data", "test_operations.json")


def test_notfound_file():
    result = open_excel_file("../data/test_operations_1.xlsx")
    assert result == "Файл не найден"


def test_open_file():
    result = open_excel_file(test_path_excel)
    assert result.to_dict() == {
        "MCC": {0: 4112},
        "Бонусы (включая кэшбэк)": {0: 70},
        "Валюта операции": {0: "RUB"},
        "Валюта платежа": {0: "RUB"},
        "Дата операции": {0: "30.12.2021"},
        "Дата платежа": {0: "30.12.2021"},
        "Категория": {0: "Другое"},
        "Кэшбэк": {0: 70},
        "Номер карты": {0: "*4556"},
        "Округление на инвесткопилку": {0: 0},
        "Описание": {0: "РЖД"},
        "Статус": {0: "OK"},
        "Сумма операции": {0: -1411.4},
        "Сумма операции с округлением": {0: 1411.4},
        "Сумма платежа": {0: -1411.4},
    }


def test_none_file():
    result = open_excel_file(test_path_excel_none)
    assert result.to_dict() == {}


def test_file_write():
    result = write_to_file(open_excel_file(test_path_excel).to_dict(), path_operations_test)
    assert result == "Данные записаны в Ваш файл"
