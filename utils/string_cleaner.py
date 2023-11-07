import re
from utils.config import ConfigImporter
from utils.string_formatter import StringFormatter

class StringCleaner:

    config = ConfigImporter()

    def __init__(self) -> None:
            self._cleaned_string = None


    def clean(self, string_to_clean:str) -> str:
        
        self._cleaned_string = StringFormatter().format(string_to_clean)
    
        if self._is_zipcode_plus_city():
            return None

        self._remove_legal_statuses()
        self._cleaned_string = self._cleaned_string.strip()

        return self._cleaned_string


    def _remove_legal_statuses(self) -> None :
        for legal_status_regex in self.config.data["legal_statuses"].values():
            self._cleaned_string = re.sub(legal_status_regex, "", self._cleaned_string)


    def _is_zipcode_plus_city(self) :
         return re.search(self.config.data["zipcode_plus_city"], self._cleaned_string) != None
