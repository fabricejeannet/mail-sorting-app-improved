import re
import logging
from fuzzywuzzy import fuzz
from utils.config import ConfigImporter
from utils.string_formatter import StringFormatter

class StringCleaner:

    config = ConfigImporter()

    def __init__(self) -> None:   
        self._cleaned_string = None


    def clean(self, string_to_clean:str) -> str:
        if self._is_not_a_relevant_string(string_to_clean) :
            return None
        
        self._cleaned_string = StringFormatter().format(string_to_clean)
        self._remove_legal_statuses()
        self._cleaned_string = self._cleaned_string.strip()
        return self._cleaned_string


    def _remove_legal_statuses(self) -> None :
        for legal_status_regex in self.config.data["legal_statuses"].values():
            self._cleaned_string = re.sub(legal_status_regex, "", self._cleaned_string)


    def _is_not_a_relevant_string (self, string_to_check:str) -> bool :
        logging.debug("Checking if " + string_to_check  + " is a non relevant word...") 
        non_relevant_strings = self.config.data["non_relevant_strings"]
        non_relevant_word_found = False
        index = 0
        while (not non_relevant_word_found and index < len(non_relevant_strings)) :
            ratio = fuzz.ratio(string_to_check, non_relevant_strings[index])
            print("\t partial_ratio ("+ string_to_check + ", " + non_relevant_strings[index] + ") = " + str(ratio) )
            non_relevant_word_found = ratio > self.config.data["thresholds"]["non_relevant_string_ratio"]
            index += 1
        
        print("Non relevant  = " + str(non_relevant_word_found))
        return non_relevant_word_found