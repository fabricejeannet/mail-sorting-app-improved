from utils.string_cleaner import StringCleaner
from utils.string_formatter import StringFormatter
from utils.config import ConfigImporter
from fuzzywuzzy import fuzz

class Matcher:
    
    config = ConfigImporter()
    string_cleaner = StringCleaner()
    string_formatter = StringFormatter()

    def __init__(self, data_frame) :
        self._data_frame = data_frame

    
    def get(self, given_string:str) -> [] :
        cleaned_string = self.string_cleaner.clean(given_string)
        print("Searching for \"" + cleaned_string + "\" (" + given_string + ") :")

        if cleaned_string is None:
            print("Non relevant string, matching aborted.")
            return None
        
        rows = []
        company_names = self._data_frame[self.config.data["csv_headers"]["company_name"]]
        for index, company_name in enumerate(company_names):
            if fuzz.ratio(cleaned_string, self.string_formatter.format(company_name)) == 100:
                print("Matching company_name at index[" + str(index) + "] : " + company_name)
                rows.append(self._data_frame.iloc[index])
        
        print(str(len(rows)) + " tuple(s) found")
   
        return rows

