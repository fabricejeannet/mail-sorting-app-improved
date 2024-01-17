import cv2

class MSIImage :

    def __init__(self, rgb_image) :
        self.rgb_image = rgb_image
        self.prepared_image = self.prepare_image_for_ocr()
    
    def prepare_image_for_ocr(self) :
        prepared_image = cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2GRAY)
        prepared_image = cv2.medianBlur(prepared_image,1)
        return prepared_image



            