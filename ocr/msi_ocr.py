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
        already_treated_lines = []

        for line_num, words_found in dataframe.groupby(["block_num", "par_num","line_num"]):
            
            # filter out words with a low confidence
            words_found = words_found[words_found["conf"] >= CONFIDENCE_THRESHOLD]
            if not len(words_found):
                continue

            words = words_found["text"].values
            line = " ".join(words)
            #logging.info(f"Line #{line_num} : {line}")

            if not line.strip():
                continue
                
            cleaned_line = self._string_cleaner.clean(line)
            
            if not cleaned_line:
                continue

            if cleaned_line in already_treated_lines:
                continue

            logging.info(f"Cleaned Line : {cleaned_line}")
            logging.info(f"words_per_line :\n{words_found}")
            
            y = CROPPED_IMAGE_BOTTOM_RIGHT_CORNER[1]
            x = CROPPED_IMAGE_BOTTOM_RIGHT_CORNER[0]
            h = 0
            w = 0

            for left, top, width, height in words_found[["left", "top", "width", "height"]].values:
                if top < y :
                    y = top
                if left < x : 
                    x = left
            
                if height > h :
                    h = height

                w += ((left - (x + w)) + width)

            ocr_result = OcrResult(cleaned_line, x, y, w, h)
            already_treated_lines.append(cleaned_line)
            results.append(ocr_result)

            #logging.info(f"Bouding box :\n{bounding_box}")

          

        return results