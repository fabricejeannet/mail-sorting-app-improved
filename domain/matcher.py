from utils.string_cleaner import StringCleaner
from utils.string_formatter import StringFormatter
from utils.config import ConfigImporter
from fuzzywuzzy import fuzz
from domain.result import Result
from domain.csv_file import CsvFile
from utils.constants import *

class Matcher:
    
    string_cleaner = StringCleaner()
    string_formatter = StringFormatter()

    def __init__(self, csv_file:CsvFile) :
        self._data_frame = csv_file.get_dataframe()

    
    def get(self, given_string:str) -> [] :
        cleaned_string = self.string_cleaner.clean(given_string)
        print("Searching for \"" + cleaned_string + "\" (" + given_string + ") :")

        if cleaned_string is None:
            print("Non relevant string, matching aborted.")
            return None

        
        results = []
        company_names = self._data_frame[COMPANY_NAME]

        for index, company_name in enumerate(company_names):
            if fuzz.ratio(cleaned_string, company_name) == 100:
                print("Matching company_name at index[" + str(index) + "] : " + company_name)
                
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
                results.append(result)
                print(str(result))
        
        print(str(len(results)) + " result(s) found")
   
        return results

