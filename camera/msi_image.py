import cv2
from utils.constants import *

class MSIImage :

    def __init__(self, rgb_image) :
        self.rgb_image = rgb_image
        self.prepared_image = self.prepare_image_for_ocr()
    
    def prepare_image_for_ocr(self) :
        prepared_image = self.rgb_image[TOP_LEFT_CORNER[1]:BOTTOM_RIGHT_CORNER[1],TOP_LEFT_CORNER[0]:BOTTOM_RIGHT_CORNER[0]]
        prepared_image = cv2.cvtColor(prepared_image, cv2.COLOR_BGR2GRAY)
        prepared_image = cv2.medianBlur(prepared_image,1)
        return prepared_image



            