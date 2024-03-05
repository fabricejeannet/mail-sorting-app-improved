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


    def extract_text(self, prepared_image) :
        
        dataframe = pytesseract.image_to_data(prepared_image, lang=LANGUAGE, output_type=pytesseract.Output.DATAFRAME)
        ocr_results:list[OcrResult] = []

        logging.info(dataframe)

        for line_num, words_found in dataframe.groupby(["block_num", "par_num","line_num"]):
            
            words_found = words_found[words_found["conf"] >= CONFIDENCE_THRESHOLD]
            if not len(words_found):
                continue
               
            words = words_found["text"].values
            line = " ".join(words)
            
            if not line.strip():
                continue

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
        
            ocr_results.append(OcrResult(line, x, y, w, h))

        return ocr_results
    

    def _discard_duplicates(self, ocr_results:list[OcrResult]):
        already_read_texts = []
        filtered_ocr_results = []
        for ocr_result in ocr_results:
            
            if ocr_result.read_text in already_read_texts:
                ocr_result.discard()

            filtered_ocr_results.append(ocr_result)
            already_read_texts.append(ocr_result.read_text)


    def _discard_non_relevant_lines(self, ocr_results:list[OcrResult]):
        for ocr_result in ocr_results:
            if self._string_cleaner._is_not_a_relevant_string(ocr_result.read_text):
                ocr_result.discard()
            else:
                ocr_result.clean_text = self._string_cleaner.clean(ocr_result.read_text)

   