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
                logging.debug(f"Searching matches for {ocr_result.clean_text} :")
                matches += self._get_match_for_string(ocr_result.clean_text)
        
        logging.debug(f"{len(matches)} matches found.")

        self._remove_duplicate_companies(matches)
        
        if self._perfect_match_found:
            logging.debug("At least one perfect match found !")
            self._remove_match_with_no_perfect_ratio(matches)

        matches = sorted(matches, key=lambda match: match.get_max_ratio(), reverse=True)
        return matches


    def _get_match_for_string(self, cleaned_string:str)  :
        matches = []
        ids = self._data_frame[ID]
        for index, id in enumerate(ids):          
            for column in [COMPANY_NAME, TRADEMARK, OWNER]:
                matches += self._search_for_match_in_column(cleaned_string, column, index, id)
        
        return matches


    def _remove_duplicate_companies(self, matches:List[Match]):
        logging.debug("------ Removing duplicates companies ------")
        used_ids = []
        matches_copy = matches.copy()
        for match in matches_copy:
            if match.id in used_ids :
                logging.debug(f"{match.company_name}[{match.id}] removed.")
                matches.remove(match)
                used_ids.append(match.id)


    def _remove_match_with_no_perfect_ratio(self, matches:List[Match]):
        logging.debug("------ Removing match with no perfect ratio ------")
        matches_copy = matches.copy()
        for match in matches_copy:
            logging.debug(f"Analyzing match [{match.company_name}]")

            if 100.0 not in match.matching_ratio.values():
                matches.remove(match)
                logging.debug("100% not match found, removing it.")
            else:
                logging.debug("100% match found, keeping it.")

        

    def _search_for_match_in_column(self, given_string:str, column:str, index:int, id) :
        name_list = self._data_frame[column].iloc[index]
        matches = []

        for name in name_list.split(';'):
            standard_ratio = round(fuzz.ratio(given_string, name))
            token_set_ratio = round(fuzz.token_set_ratio(given_string, name))
            token_sort_ratio = round(fuzz.token_sort_ratio(given_string, name))
           
            ratio = max(standard_ratio, max(token_set_ratio, token_sort_ratio))

            if not self._perfect_match_found:
                self._perfect_match_found = ratio == 100.0
                if self._perfect_match_found:
                    logging.debug("****** Perfect match found ! ******")

            if ratio >= MATCHING_THRESHOLD:
                logging.debug(f"Match found comparing [{id}]'{given_string}' to '{name}' in column [{column}] : ratio = {standard_ratio}, token_sort_ratio = {token_sort_ratio}, , token_set_ratio = {token_set_ratio}")

                if id not in self._id_match_dict.keys():
                    logging.debug("Creating new match.")
                    match = self._create_match_from_row_index(index)
                    matches.append(match)
                    self._id_match_dict[id] = match
                else :
                    match = self._id_match_dict.get(id)
                    logging.debug(f"Updating existing match [{match.id}]")
                
                match.matching_ratio[column] = ratio
            
        return matches


    def _create_match_from_row_index(self, index:int) -> Match :
        match = Match()
        match.id = self._data_frame.iloc[index][ID]
        match.status = self._data_frame.iloc[index][STATUS]
        match.company_name = self._data_frame.iloc[index][COMPANY_NAME]
        if self._data_frame.iloc[index][TRADEMARK] != None:
            match.trademark =self._data_frame.iloc[index][TRADEMARK].split(";")
            logging.debug(f"Split Trademark : {match.trademark}  ")
        else:
            match.trademark = []
        match.owner = self._data_frame.iloc[index][OWNER]
        match.domiciliary = self._data_frame.iloc[index][DOMICILIARY]   
        return match  

'''
    def _split_list_of_names(self, str_to_split) :

        print(f"Trying to split '{str_to_split}'")
        separators = [";", ",", "-"]
        separator_found = False
        index = -1

        while not separator_found and index < len(separators) - 1:
            index += 1
            separator_found = separators[index] in str_to_split
        
        if separator_found:
            print(f"Separator'{separators[index]}' found")

            list_of_trademarks =  str_to_split.split(separators[index])
            for index, trademark in enumerate(list_of_trademarks):
                list_of_trademarks[index] = trademark.strip()
            print(f"'{str_to_split}' split to '{list_of_trademarks}'")

            return list_of_trademarks
        
        print(f"No separator found, returning '{str_to_split}'")

        return [str_to_split]
'''