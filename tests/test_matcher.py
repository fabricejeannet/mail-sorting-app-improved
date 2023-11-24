from domain.matcher import Matcher
import pandas as pd
from domain.csv_file import CsvFile
from utils.constants import *


csv_file = CsvFile("test.csv")
matcher = Matcher(csv_file)

def test_returns_a_100_percent_matching_company_name_tuple():
    results = matcher.get("cosy wine")
    assert len(results) == 1
    assert results[0].id == 1
    assert results[0].status == SUBSCRIBED
    assert results[0].company_name == "cosy wine"
    assert results[0].trademark == ["on s occupe du vin"]
    assert results[0].owner == "gregoire domingie"
    assert results[0].domiciliary == "coolworking"


def test_returns_a_100_percent_matching_trademark():
    results = matcher.get("Horizon Prévention")
    assert len(results) == 1
    assert results[0].company_name == "helloprev"

