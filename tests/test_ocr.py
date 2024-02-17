
import os
import cv2
from camera.msi_image import MSIImage
from ocr.msi_ocr import *
import numpy as np
import cv2
import inspect 

msi_ocr = MSIOcr()
temp_dir_path = os.path.abspath(f"{os.getcwd()}/temp//")
root_path = os.path.abspath(f"{os.getcwd()}/")


def test_can_read_clean_image() :
    rgb_image = create_fake_enveloppe(["Text to read"])
    msi_image =  MSIImage(rgb_image)
    save_image(msi_image)
    results = msi_ocr.perform_on(msi_image.prepared_image)
    assert len(results) == 1
    assert results[0].text == "text to read"


def test_removes_street_and_zipcode_line() :
    rgb_image = create_fake_enveloppe(["Fleur de Vie", "9 rue de Conde", "33000 Bordeaux"])
    msi_image =  MSIImage(rgb_image)
    save_image(msi_image)
    results = msi_ocr.perform_on(msi_image.prepared_image)
    assert len(results) == 1
    assert results[0].text == "fleur de vie"
  

def test_removes_duplicate_lines_in_address() :
    rgb_image = create_fake_enveloppe(["Ma super boite", "Ma super boite", "9 rue de Conde", "33000 Bordeaux"])
    msi_image =  MSIImage(rgb_image)
    save_image(msi_image)
    results = msi_ocr.perform_on(msi_image.prepared_image)
    assert len(results) == 1
    assert results[0].text == "ma super boite"
  


def create_fake_enveloppe(text:[]):
    fake_enveloppe = np.full((CAMERA_PREVIEW_HEIGHT, CAMERA_PREVIEW_WIDTH, 4), 255, dtype=np.uint8)
    y = CROPPED_IMAGE_TOP_LEFT_CORNER[1] + 30
    for line in text:
        cv2.putText (img=fake_enveloppe, text=line, org=(CROPPED_IMAGE_TOP_LEFT_CORNER[0] + 10,  y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(0, 0, 255,100), thickness=2)
        y += 25    
    fake_enveloppe = cv2.cvtColor(fake_enveloppe, cv2.COLOR_BGR2RGB)
    return fake_enveloppe


def save_image(msi_image:MSIImage) -> None :
    calling_function_name = (inspect.stack()[1][3]) 
    cv2.imwrite(temp_dir_path + f"/{calling_function_name}_rgb.jpg", msi_image.rgb_image)
    cv2.imwrite(temp_dir_path + f"/{calling_function_name}_prepared.jpg", msi_image.prepared_image) 