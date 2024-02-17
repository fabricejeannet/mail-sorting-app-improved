from domain.matcher import Matcher
import pandas as pd
from domain.csv_file import CsvFile
from utils.constants import *
from ocr.ocr_result import OcrResult
import os

filepath = os.path.abspath(f"{os.getcwd()}/tests/test.csv")
csv_file = CsvFile(filepath)
matcher = Matcher(csv_file)


def test_finds_a_100percent_matching_company_name():
    matches = matcher._get_match_for_string("cosy wine")
    assert len(matches) == 1
    assert matches[0].id == 1
    assert matches[0].status == SUBSCRIBED
    assert matches[0].company_name == "cosy wine"
    assert matches[0].trademark == ["on s occupe du vin"]
    assert matches[0].owner == "gregoire domingie"
    assert matches[0].domiciliary == "coolworking"


def test_finds_two_100_percent_matching_trademark():
    matches = matcher._get_match_for_string("Horizon Prévention")
    assert len(matches) == 1
    assert matches[0].company_name == "helloprev"
    matches = matcher._get_match_for_string("oprev")
    assert len(matches) == 1
    assert matches[0].company_name == "helloprev"


def test_finds_two_100_percent_matching_owners():
    matches = matcher._get_match_for_string("Simon")
    assert len(matches) == 1
    assert matches[0].company_name == "sound of silence"
    matches = matcher._get_match_for_string("Garfunkel")
    assert len(matches) == 1
    assert matches[0].company_name == "sound of silence"


def test_finds_a_100_percent_matching_owner():
    matches = matcher._get_match_for_string("Chahir Halitim")
    assert len(matches) == 1
    assert matches[0].company_name == "helloprev"


def test_returns_two_results_for_fabrice_jeannet_as_the_owner():
    matches = matcher._get_match_for_string("Fabrice JEANNET")
    assert len(matches) == 2
    assert matches[0].company_name == "coolworking"
    assert matches[1].company_name == "linkinsport"


def test_finds_an_owner_with_last_name_and_first_name_reversed():
    matches = matcher._get_match_for_string("Halitim Chahir")
    assert len(matches) == 1
    assert matches[0].company_name == "helloprev"


def test_finds_an_owner_approximated_name():
    matches = matcher._get_match_for_string("Gregory Domingie")
    assert len(matches) == 1
    assert matches[0].company_name == "cosy wine"
    assert matches[0].matching_ratio[OWNER] >= OWNER_MATCHING_THRESHOLD

    matches = matcher._get_match_for_string("goire Doming")
    assert len(matches) == 1
    assert matches[0].company_name == "cosy wine"
    assert matches[0].matching_ratio[OWNER] >= OWNER_MATCHING_THRESHOLD

    matches = matcher._get_match_for_string("garfun")
    assert len(matches) == 1
    assert matches[0].company_name == "sound of silence"
    assert matches[0].matching_ratio[OWNER] >= OWNER_MATCHING_THRESHOLD


def test_finds_a_company_approximated_name():
    matches = matcher._get_match_for_string("ordeaux ren")
    assert len(matches) == 1
    assert matches[0].company_name == "bordeaux renov"
    assert matches[0].matching_ratio[COMPANY_NAME] >= OWNER_MATCHING_THRESHOLD


def test_finds_a_match_from_an_array_of_OcrResults():
    ocr_results =[ OcrResult("Françoise Sanquer", 0, 0, 40, 10), OcrResult("Bordeaux Renov", 0, 0, 40, 10), OcrResult("9 rue de Condé ", 0, 0, 40, 10), OcrResult("33000 Bordeaux", 0, 0, 40, 10) ]
    matches = matcher.get_match_for_ocr_results(ocr_results)
    assert len(matches) == 1
    assert matches[0].company_name == "bordeaux renov"


def test_result_curation():
    r0 = matcher._create_result_from_row_index(0)
    r1 = matcher._create_result_from_row_index(1)
    r2 = matcher._create_result_from_row_index(2)

    mock_results = [r0, r1, r0, r2, r2]
    curracted_mock_results = matcher._remove_duplicate(mock_results)
    assert len(curracted_mock_results) == 3
    assert curracted_mock_results[0] == r0
    assert curracted_mock_results[1] == r1
    assert curracted_mock_results[2] == r2


def test_feeding_an_empty_list_of_string_returns_an_empty_list_of_results():
    results = matcher.get_match_for_ocr_results([])
    assert len(results) == 0