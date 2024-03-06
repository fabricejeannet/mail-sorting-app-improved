import re
import logging
from fuzzywuzzy import fuzz
#from utils.config import ConfigImporter
from unidecode import unidecode
from utils.constants import *


class StringCleaner:

    config = ConfigImporter()

    def __init__(self) -> None:   
        pass

    def _remove_unnecessary_whitespaces(self, given_string) -> str :
        return re.sub("\\s{2,}", " ", given_string).strip()   


    #TODO Might be faster to stop after the first occurence of a legal status
    def _remove_legal_statuses(self, given_string:str) -> str :
        for legal_status_regex in LEGAL_STATUSES.values() :
            given_string = re.sub(legal_status_regex, "", given_string)
        return given_string


    def _is_not_a_relevant_string (self, string_to_check:str) -> bool :

        if self._is_a_postal_digit_sequence(string_to_check):
            return True

        string_to_check = string_to_check.lower()
        logging.debug("Checking if " + string_to_check  + " is a non relevant word...") 
        non_relevant_word_found = False
        index = 0
        while (not non_relevant_word_found and index < len(NON_RELEVANT_STRINGS)) :
            ratio = fuzz.ratio(string_to_check, NON_RELEVANT_STRINGS[index])
            logging.debug("\t partial_ratio ("+ string_to_check + ", " + NON_RELEVANT_STRINGS[index] + ") = " + str(ratio) )
            non_relevant_word_found = ratio > NON_RELEVANT_STRINGS_RATIO
            index += 1
        
        logging.debug("Non relevant  = " + str(non_relevant_word_found))
        return non_relevant_word_found
    

    def _is_a_postal_digit_sequence(self, string_to_check:str) -> bool :
        return re.search(DIGIT_SEQUENCE, string_to_check) != None


    def _replace_amperstamp_with_et(self, given_string) -> str :
        return given_string.replace("&", " et ")


    def _remove_special_characters_except_semicolon(self, given_string) -> str :        
        return re.sub("[^;a-zA-Z\\d\\s]", " ", given_string)


    def _remove_accents(self, given_string) -> str :
        return unidecode(given_string)


    def _remove_special_characters(self, given_string) -> str :        
        return re.sub("[\\W_]", " ", given_string)


    def _remove_gender_marks(self, given_string) -> str :
        return re.sub(GENDER_MARKS, " ", given_string)

    def format(self, string_to_format:str) -> str :    
        formatted_string = self._replace_amperstamp_with_et(string_to_format)
        formatted_string = self._remove_special_characters(formatted_string)
        formatted_string = formatted_string.lower()
        formatted_string = self._remove_accents(formatted_string)
        formatted_string = self._remove_gender_marks(formatted_string)
        formatted_string = self._remove_unnecessary_whitespaces(formatted_string)
        return formatted_string



    def clean_for_csv(self, string_to_clean:str) -> str:
        clean_string = string_to_clean
        clean_string = self._remove_legal_statuses(clean_string)
        clean_string = self.format_for_csv(clean_string)
        clean_string = self._remove_unnecessary_whitespaces(clean_string)
        return clean_string


    def clean(self, string_to_clean:str) -> str:
        clean_string = string_to_clean
        clean_string = self._remove_legal_statuses(clean_string)
        clean_string = self.format(clean_string)
        clean_string = self._remove_unnecessary_whitespaces(clean_string)
        return clean_string


    def format_for_csv(self, string_to_format:str) -> str :    
        formatted_string = self._replace_amperstamp_with_et(string_to_format)
        formatted_string = self._remove_accents(formatted_string)
        formatted_string = self._remove_special_characters_except_semicolon(formatted_string)
        formatted_string = formatted_string.lower()
        formatted_string = self._remove_gender_marks(formatted_string)
        formatted_string = self._remove_unnecessary_whitespaces(formatted_string)
        formatted_string = self._remove_unnecessary_whitespaces(formatted_string)
        return formatted_string
