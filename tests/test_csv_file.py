from csv_file.csv_file import CsvFile
import os

def test_csv_file_is_cleaned() :
    filepath = os.path.abspath(f"{os.getcwd()}/tests/test.csv")
    csv_file = CsvFile(filepath)
    assert csv_file._data_frame["company_name"][0] == "bordeaux renov"

def test_split():
    test_str = ""
    assert test_str.split(";") == ['']

