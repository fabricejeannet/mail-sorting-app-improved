
import os
import cv2
from camera.msi_image import MSIImage
from ocr.msi_ocr import *

msi_ocr = MSIOcr()

def test_can_read_clean_image() :
    image_filepath = os.path.abspath(f"{os.getcwd()}/tests/img/clean-fleur-de-vie.png")
    rgb_image =   cv2.cvtColor(cv2.imread(image_filepath), cv2.COLOR_BGR2RGB)
    msi_image =  MSIImage(rgb_image)

    root_path = os.path.abspath(f"{os.getcwd()}/")

    cv2.imwrite(root_path + "/rgb.jpg", msi_image.rgb_image)
    cv2.imwrite(root_path + "/prepared.jpg", msi_image.prepared_image) 

    results = msi_ocr.perform_on(msi_image.prepared_image)
    assert len(results) == 1
    assert results[0].line == "fleur de vie"
