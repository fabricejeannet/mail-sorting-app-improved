from utils.string_cleaner import StringCleaner
from utils.config import ConfigImporter
from fuzzywuzzy import fuzz
from domain.match import Match
from domain.csv_file import CsvFile
from utils.constants import *
from ocr.ocr_result import OcrResult
from typing import List

class Matcher:
    
    string_cleaner = StringCleaner()

    def __init__(self, csv_file:CsvFile) :
        self._data_frame = csv_file.get_dataframe()
     
   
    def get_match_for_ocr_results(self, ocr_results:List[OcrResult]) :
        matches = []
        for ocr_result in ocr_results :
            if not ocr_result.is_discarded():
                matches += self._get_match_for_string(ocr_result.clean_text)
        
        return self._remove_duplicate_companies(matches)


    def _get_match_for_string(self, cleaned_string:str)  :
        matches = []
        ids = self._data_frame[ID]
        for index, id in enumerate(ids):          
            for column in [COMPANY_NAME, TRADEMARK, OWNER]:
                matches += self._search_for_match_in_column(cleaned_string, column, index)
        
        return matches


    def _remove_duplicate_companies(self, ocr_results:List[OcrResult])  :
        used_ids = []
        currated_ocr_results = []
        for ocr_result in ocr_results:
            if not (ocr_result.id in used_ids) :
                currated_ocr_results.append(ocr_result)
                used_ids.append(ocr_result.id)
        return currated_ocr_results


    def _search_for_match_in_column(self, given_string:str, column:str, index:int) :
        name_list = self._data_frame[column].iloc[index]
        matches = []
        for name in name_list.split(';'):
            ratio = max(fuzz.ratio(given_string, name), fuzz.token_sort_ratio(given_string, name))
            if ratio >= OWNER_MATCHING_THRESHOLD:
                match = self._create_match_from_row_index(index)
                match.matching_ratio[column] = ratio
                matches.append(match)
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
