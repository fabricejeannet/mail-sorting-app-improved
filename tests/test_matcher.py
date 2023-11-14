from domain.matcher import Matcher
import pandas as pd
from domain.csv_file import CsvFile


csv_file = CsvFile("test.csv")
matcher = Matcher(csv_file)

def test_returns_a_100_percent_matching_company_name_tuple():
    tuple = matcher.get("Bordeaux Rénov")
    assert len(tuple) == 1
    assert tuple[0][2] == "bordeaux renov"
