from utils.string_cleaner import StringCleaner
from utils.config import ConfigImporter
from rapidfuzz import fuzz
from matcher.match import Match
from csv_file.csv_file import CsvFile
from utils.constants import *
from ocr.ocr_result import OcrResult
from typing import List
import logging
from icecream import ic

class Matcher:
    
    string_cleaner = StringCleaner()

    def __init__(self, csv_file:CsvFile) :
        self._data_frame = csv_file.get_dataframe()
        self._id_match_dict = {}
        self._perfect_match_found = False

   
    def get_match_for_ocr_results(self, ocr_results:List[OcrResult]) :
        self._id_match_dict.clear()
        self._perfect_match_found = False

        matches = []
        for ocr_result in ocr_results :
            if not ocr_result.is_discarded():
                logging.debug(f"Searching match for {ocr_result.clean_text} :")
                matches += self._get_match_for_string(ocr_result.clean_text)
        self._remove_duplicate_companies(matches)
        
        matches = sorted(matches, key=lambda match: match.get_max_ratio(), reverse=True)
        return matches


    def _get_match_for_string(self, cleaned_string:str)  :
        matches = []
        ids = self._data_frame[ID]
        for index, id in enumerate(ids):          
            for column in [COMPANY_NAME, TRADEMARK, OWNER]:
                matches += self._search_for_match_in_column(cleaned_string, column, index, id)
        
        return matches


    def _remove_duplicate_companies(self, ocr_results:List[OcrResult]):
        used_ids = []
        currated_ocr_results = []
        for ocr_result in ocr_results:
            if not (ocr_result.id in used_ids) :
                currated_ocr_results.append(ocr_result)
                used_ids.append(ocr_result.id)
            
        #return currated_ocr_results


    def _remove_match_with_no_perfect_ratio(self, matches:List[Match]):
        currated_matches = []
        for match in matches:
            if 100 in match.matching_ratio.values():
                currated_matches.append(match)
        matches = currated_matches



    def _search_for_match_in_column(self, given_string:str, column:str, index:int, id) :
        name_list = self._data_frame[column].iloc[index]
        matches = []
        for name in name_list.split(';'):
            #standard_ratio = fuzz.ratio(given_string, name)
            #token_ratio =  fuzz.token_sort_ratio(given_string, name)
            #ratio = max(standard_ratio, token_ratio)

            # Algo de Loïc
            standard_ratio = fuzz.ratio(given_string, name)
            token_ratio =  (fuzz.token_set_ratio(given_string, name) + fuzz.token_sort_ratio(given_string, name)) / 2.0
            ratio = (standard_ratio + fuzz.partial_ratio(given_string, name) * 2 + token_ratio * 2) / 5.0

            if ratio >= OWNER_MATCHING_THRESHOLD:
                logging.debug(f"Match found comparing '{given_string}' to '{name}' in column '{column}' : standard ratio = {standard_ratio}, token ratio = {token_ratio}")
                print(f"Match found comparing '{given_string}' to '{name}' in column '{column}' : standard ratio = {standard_ratio}, token ratio = {token_ratio}")
                
                if id not in self._id_match_dict.keys():
                    match = self._create_match_from_row_index(index)
                    match.matching_ratio[column] = ratio
                    matches.append(match)
                    self._id_match_dict[id] = match
                else :
                    match = self._id_match_dict.get(id)
                
                match.matching_ratio[column] = ratio

        return matches


    def _create_match_from_row_index(self, index:int) -> Match :
        match = Match()
        match.id = self._data_frame.iloc[index][ID]
        match.status = self._data_frame.iloc[index][STATUS]
        match.company_name = self._data_frame.iloc[index][COMPANY_NAME]
        if self._data_frame.iloc[index][TRADEMARK] != None:
            match.trademark = str(self._data_frame.iloc[index][TRADEMARK]).split(";")
        else:
            match.trademark = []
        match.owner = self._data_frame.iloc[index][OWNER]
        match.domiciliary = self._data_frame.iloc[index][DOMICILIARY]   
        return match  
