import re
from unidecode import unidecode
from utils.config import ConfigImporter
    
class StringFormatter:
    
    config = ConfigImporter()


    def __init__(self) -> None:
        self._formatted_string = None
    

    def format(self, string_to_format:str) -> str : 
        self._formatted_string = string_to_format
        self._replace_amperstamp_with_et()
        self._remove_special_characters()
        self._formatted_string = self._formatted_string.lower()
        self._remove_accents()
        self._remove_legal_statuses()
        self._reduce_spaces_between_words_to_one()
        self._formatted_string = self._formatted_string.strip()

        return self._formatted_string


    def _remove_legal_statuses(self) -> None :
        for legal_status_regex in self.config.data["legal_statuses"].values():
            print(legal_status_regex)
            self._formatted_string = re.sub(legal_status_regex, " ", self._formatted_string)
    

    def _replace_amperstamp_with_et(self) -> None :
        self._formatted_string = self._formatted_string.replace("&", " et ")


    def _remove_special_characters(self) -> None :
        self._formatted_string = re.sub("[\\W_]", " ", self._formatted_string)


    def _remove_accents(self) -> None :
        self._formatted_string = unidecode(self._formatted_string)


    def _reduce_spaces_between_words_to_one(self) -> None :
        self._formatted_string = re.sub("\\s{2,}", " ", self._formatted_string)


