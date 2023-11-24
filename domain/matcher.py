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

    
    def get(self, given_string:str) -> [] :
        cleaned_string = self.string_cleaner.clean(given_string)
        print("Searching for \"" + cleaned_string + "\" (" + given_string + ") :")

        if cleaned_string is None:
            print("Non relevant string, matching aborted.")
            return None
        
        results = []
        results += self._search_for_company_name_matching(cleaned_string)
        results += self._search_for_trademark_matching(cleaned_string)
        return results
    

    def _search_for_company_name_matching(self, given_string:str) :
        results = []
        company_names = self._data_frame[COMPANY_NAME]
        for index, company_name in enumerate(company_names):
            if fuzz.ratio(given_string, company_name) == 100:
                print("Matching company_name at index[" + str(index) + "] : " + company_name)           
                result = self._create_result_from_row_index(index)
                results.append(result)
        return results
    
   
    def _search_for_trademark_matching(self, given_string:str) :
        results = []
        trademark_lists = self._data_frame[TRADEMARK]
        for index, trademark_list in enumerate(trademark_lists): 
            print("trademarks [" + str(index) + "] : " + trademark_list)
            for trademark in trademark_list.split(';'):
                if fuzz.ratio(given_string, trademark) == 100:
                    print("Matching trademark at index[" + str(index) + "] : " + trademark)           
                    result = self._create_result_from_row_index(index)
                    results.append(result)
                    break
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
