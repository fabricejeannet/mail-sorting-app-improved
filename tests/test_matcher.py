from matcher.matcher import Matcher
import pandas as pd
from csv_file.csv_file import CsvFile
from utils.constants import *
from ocr.ocr_result import OcrResult
from utils.string_cleaner import StringCleaner
import os
from typing import List

filepath = os.path.abspath(f"{os.getcwd()}/tests/test.csv")
csv_file = CsvFile(filepath)
matcher = Matcher(csv_file)
string_cleaner = StringCleaner()


def get_list_of_fake_ocr_results(read_texts:List[str]) -> List[OcrResult]:
    ocr_results = []
    for read_text in read_texts:
        ocr_results.append(get_fake_ocr_result(read_text))
    return ocr_results


def get_fake_ocr_result(read_text:str) -> OcrResult:
    ocr_result:OcrResult = OcrResult(read_text, 0, 0, 50, 10)
    ocr_result.clean_text = string_cleaner.clean(read_text)
    return ocr_result


def test_finds_a_100percent_matching_company_name():
    matches = matcher.get_match_for_ocr_results(get_list_of_fake_ocr_results(["Cosy wine"]))
    assert len(matches) == 1
    assert matches[0].id == 1
    assert matches[0].status == SUBSCRIBED
    assert matches[0].company_name == "cosy wine"
    assert matches[0].trademark == ["on s occupe du vin"]
    assert matches[0].owner == "gregoire domingie"
    assert matches[0].domiciliary == "coolworking"
    assert matches[0].matching_ratio[COMPANY_NAME] == 100


def test_finds_two_100_percent_matching_trademark():
    matches = matcher.get_match_for_ocr_results(get_list_of_fake_ocr_results(["Horizon Prévention"]))
    assert len(matches) == 1
    assert matches[0].company_name == "helloprev"
    assert matches[0].matching_ratio[TRADEMARK] == 100

    matches = matcher.get_match_for_ocr_results(get_list_of_fake_ocr_results(["Oprev"]))
    assert len(matches) == 1
    assert matches[0].company_name == "helloprev"
    assert matches[0].matching_ratio[TRADEMARK] == 100


def test_matcher_returns_only_one_result_for_matching_company_name_and_owner():
    matches = matcher.get_match_for_ocr_results(get_list_of_fake_ocr_results(["Helloprev", "Chahir Halitim"]))
    assert len(matches) == 1
    assert matches[0].company_name == "helloprev"
    assert matches[0].matching_ratio[COMPANY_NAME] == 100
    assert matches[0].matching_ratio[OWNER] == 100



def test_finds_two_100_percent_matching_owners():
    matches = matcher.get_match_for_ocr_results(get_list_of_fake_ocr_results(["Simon"]))
    assert len(matches) == 1
    assert matches[0].company_name == "sound of silence"
    matches = matcher.get_match_for_ocr_results(get_list_of_fake_ocr_results(["Garfunkel"]))
    assert len(matches) == 1
    assert matches[0].company_name == "sound of silence"


def test_finds_a_100_percent_matching_owner():
    matches = matcher.get_match_for_ocr_results(get_list_of_fake_ocr_results(["Chahir Halitim"]))
    assert len(matches) == 1
    assert matches[0].company_name == "helloprev"
    assert matches[0].matching_ratio[OWNER] == 100


def test_returns_two_results_for_fabrice_jeannet_as_the_owner():
    matches = matcher._get_match_for_string("Fabrice JEANNET")
    assert len(matches) == 2
    assert matches[0].company_name == "coolworking"
    assert matches[1].company_name == "linkinsport"


def test_finds_an_owner_with_last_name_and_first_name_reversed():
    matches = matcher.get_match_for_ocr_results(get_list_of_fake_ocr_results(["Chahir Halitim"]))
    assert len(matches) == 1
    assert matches[0].company_name == "helloprev"
    assert matches[0].matching_ratio[OWNER] == 100


def test_finds_an_owner_approximated_name():
    matches = matcher.get_match_for_ocr_results(get_list_of_fake_ocr_results(["Gregory Domingie"]))
    assert len(matches) == 1
    assert matches[0].company_name == "cosy wine"
    assert matches[0].matching_ratio[OWNER] >= OWNER_MATCHING_THRESHOLD

    matches = matcher.get_match_for_ocr_results(get_list_of_fake_ocr_results(["egoire Doming"]))
    assert len(matches) == 1
    assert matches[0].company_name == "cosy wine"
    assert matches[0].matching_ratio[OWNER] >= OWNER_MATCHING_THRESHOLD

    matches = matcher.get_match_for_ocr_results(get_list_of_fake_ocr_results(["Garfunk"]))
    assert len(matches) == 1
    assert matches[0].company_name == "sound of silence"
    assert matches[0].matching_ratio[OWNER] >= OWNER_MATCHING_THRESHOLD


def test_finds_a_company_approximated_name():
    matches = matcher._get_match_for_string("ordeaux ren")
    assert len(matches) == 1
    assert matches[0].company_name == "bordeaux renov"
    assert matches[0].matching_ratio[COMPANY_NAME] >= OWNER_MATCHING_THRESHOLD


def test_removes_duplicate_companies():
    matches = matcher.get_match_for_ocr_results(get_list_of_fake_ocr_results(["Coolworking", "CosyWine", "Gregoire Domingie"]))
    matcher._remove_duplicate_companies(matches)
    assert len(matches) == 2


def test_feeding_an_empty_list_of_string_returns_an_empty_list_of_results():
    matches = matcher.get_match_for_ocr_results([])
    assert len(matches) == 0


def test_only_one_match_is_found_when_a_100_percent_match_is_already_found():
    matches = matcher.get_match_for_ocr_results(get_list_of_fake_ocr_results(["BCD Construction"]))
    matcher._remove_match_with_no_perfect_ratio(matches)
    assert len(matches) == 1
