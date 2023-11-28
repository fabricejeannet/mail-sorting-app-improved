from utils.string_cleaner import StringCleaner
from utils.config import ConfigImporter
from fuzzywuzzy import fuzz
from domain.result import Result
from domain.csv_file import CsvFile
from utils.constants import *

class Matcher:
    
    string_cleaner = StringCleaner()

    def __init__(self, csv_file:CsvFile) :
        self._data_frame = csv_file.get_dataframe()
     
   
    def get_match_for_address(self, list_of_strings:[]) -> []:
        results = []
        for string in list_of_strings :
            if string:
                cleaned_string = self.string_cleaner.clean(string)
                results += self._get_match_for_string(cleaned_string)
        
        return self._remove_duplicate(results)


    def _get_match_for_string(self, cleaned_string:str) -> [] :
        results = []
        ids = self._data_frame[ID]
        for index, id in enumerate(ids):          
            for column in [COMPANY_NAME, TRADEMARK, OWNER]:
                results += self._search_for_match_in_list(cleaned_string, column, index)
        
        return results


    def _remove_duplicate(self, results:[]) -> [] :
        used_ids = []
        currated_results = []
        for result in results:
            if not (result.id in used_ids) :
                currated_results.append(result)
                used_ids.append(result.id)
        return currated_results


    def _search_for_match_in_list(self, given_string:str, column:str, index:int) :
        name_list = self._data_frame[column].iloc[index]
        results = []
        for name in name_list.split(';'):
            ratio = max(fuzz.ratio(given_string, name), fuzz.token_sort_ratio(given_string, name))
            if ratio >= OWNER_MATCHING_THRESHOLD:
                result = self._create_result_from_row_index(index)
                result.matching_ratio[column] = ratio
                results.append(result)
        return results


    def _create_result_from_row_index(self, index:int) -> Result :
        result = Result()
        result.id = self._data_frame.iloc[index][ID]
        result.status = self._data_frame.iloc[index][STATUS]
        result.company_name = self._data_frame.iloc[index][COMPANY_NAME]
        if self._data_frame.iloc[index][TRADEMARK] != None:
            result.trademark = str(self._data_frame.iloc[index][TRADEMARK]).split(";")
        else:
            result.trademark = []
        result.owner = self._data_frame.iloc[index][OWNER]
        result.domiciliary = self._data_frame.iloc[index][DOMICILIARY]   
        return result  
