import pytesseract
import cv2
from utils.constants import *
import logging
import pandas as pd
from utils.string_cleaner import StringCleaner
from ocr.ocr_result import OcrResult

class MSIOcr:
    
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super(MSIOcr, cls).__new__(cls)
        return cls.__instance
    
    
    def __init__(self):
        self._string_cleaner = StringCleaner()


    def perform_on(self, prepared_image) :
        logging.info("-- Last OCR ---")
        dataframe = pytesseract.image_to_data(prepared_image, lang=LANGUAGE, output_type=pytesseract.Output.DATAFRAME)
        
        logging.info("Dataframe\n" + str(dataframe))
         

        results = []

        for line_num, words_per_line in dataframe.groupby(["block_num", "par_num", "line_num"]):
            
            # filter out words with a low confidence
            words_per_line = words_per_line[words_per_line["conf"] >= CONFIDENCE_THRESHOLD]
            if not len(words_per_line):
                continue

            words = words_per_line["text"].values
            line = " ".join(words)
            #logging.info(f"Line #{line_num} : {line}")

            if not line.strip():
                continue
                
            cleaned_line = self._string_cleaner.clean(line)
            
            if not cleaned_line:
                continue

            logging.info(f"Cleaned Line : {cleaned_line}")

            bounding_box = []
                
            for left, top, width, height in words_per_line[["left", "top", "width", "height"]].values:
                bounding_box.append((left, top))
                bounding_box.append((left + width, top + height))

            ocr_result = OcrResult(cleaned_line, bounding_box)
            results.append(ocr_result)

        return results