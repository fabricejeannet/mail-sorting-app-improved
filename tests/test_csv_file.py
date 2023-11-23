from domain.csv_file import CsvFile

def test_csv_file_is_cleaned() :
    csv_file = CsvFile("test.csv")
    assert csv_file._data_frame["company_name"][0] == "bordeaux renov"

def test_split():
    test_str = ""
    assert test_str.split(";") == ['']

