from domain.matcher import Matcher
import pandas as pd
from domain.csv_file import CsvFile
from utils.constants import *
import os

filepath = os.path.abspath(f"{os.getcwd()}/tests/test.csv")
csv_file = CsvFile(filepath)
matcher = Matcher(csv_file)


def test_finds_a_100percent_matching_company_name():
    results = matcher._get_match_for_string("cosy wine")
    assert len(results) == 1
    assert results[0].id == 1
    assert results[0].status == SUBSCRIBED
    assert results[0].company_name == "cosy wine"
    assert results[0].trademark == ["on s occupe du vin"]
    assert results[0].owner == "gregoire domingie"
    assert results[0].domiciliary == "coolworking"


def test_finds_two_100_percent_matching_trademark():
    results = matcher._get_match_for_string("Horizon Prévention")
    assert len(results) == 1
    assert results[0].company_name == "helloprev"
    results = matcher._get_match_for_string("oprev")
    assert len(results) == 1
    assert results[0].company_name == "helloprev"


def test_finds_two_100_percent_matching_owners():
    results = matcher._get_match_for_string("Simon")
    assert len(results) == 1
    assert results[0].company_name == "sound of silence"
    results = matcher._get_match_for_string("Garfunkel")
    assert len(results) == 1
    assert results[0].company_name == "sound of silence"


def test_finds_a_100_percent_matching_owner():
    results = matcher._get_match_for_string("Chahir Halitim")
    assert len(results) == 1
    assert results[0].company_name == "helloprev"


def test_returns_two_results_for_fabrice_jeannet_as_the_owner():
    results = matcher._get_match_for_string("Fabrice JEANNET")
    assert len(results) == 2
    assert results[0].company_name == "coolworking"
    assert results[1].company_name == "linkinsport"


def test_finds_an_owner_with_last_name_and_first_name_reversed():
    results = matcher._get_match_for_string("Halitim Chahir")
    assert len(results) == 1
    assert results[0].company_name == "helloprev"


def test_finds_an_owner_approximated_name():
    results = matcher._get_match_for_string("Gregory Domingie")
    assert len(results) == 1
    assert results[0].company_name == "cosy wine"
    assert results[0].matching_ratio[OWNER] >= OWNER_MATCHING_THRESHOLD

    results = matcher._get_match_for_string("goire Doming")
    assert len(results) == 1
    assert results[0].company_name == "cosy wine"
    assert results[0].matching_ratio[OWNER] >= OWNER_MATCHING_THRESHOLD

    results = matcher._get_match_for_string("garfun")
    assert len(results) == 1
    assert results[0].company_name == "sound of silence"
    assert results[0].matching_ratio[OWNER] >= OWNER_MATCHING_THRESHOLD


def test_finds_a_company_approximated_name():
    results = matcher._get_match_for_string("ordeaux ren")
    assert len(results) == 1
    assert results[0].company_name == "bordeaux renov"
    assert results[0].matching_ratio[COMPANY_NAME] >= OWNER_MATCHING_THRESHOLD


def test_can_feed_an_array_to_the_matcher():
    results = matcher.get_match_for_address(["Françoise Sanquer", "Bordeaux Renov", "Bureau 3", "33000 Bordeaux"])
    assert len(results) == 1
    assert results[0].company_name == "bordeaux renov"


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
    results = matcher.get_match_for_address([])
    assert len(results) == 0