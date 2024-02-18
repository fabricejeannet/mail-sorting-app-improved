
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
debug_mode = True


def test_can_read_clean_image() :
    rgb_image = create_fake_enveloppe(["Coolworking", "9 rue de Conde", "33000 Bordeaux"])
    msi_image =  MSIImage(rgb_image)
    save_image(msi_image)
    ocr_results = msi_ocr.read_text(msi_image.prepared_image)
    assert len(ocr_results) == 3
    assert ocr_results[0].read_text == "Coolworking"
    assert ocr_results[1].read_text == "9 rue de Conde"
    assert ocr_results[2].read_text == "33000 Bordeaux"


def test_can_filters_parasites() :
    rgb_image = create_fake_enveloppe(["Coolworking", ")    ."])
    msi_image =  MSIImage(rgb_image)
    save_image(msi_image)
    read_lines = msi_ocr.read_text(msi_image.prepared_image)
    assert len(read_lines) == 1
    assert read_lines[0].read_text == "Coolworking"


def test_removes_duplicates():
    rgb_image = create_fake_enveloppe(["Coolworking", "Coolworking", "33000 Bordeaux"])
    msi_image =  MSIImage(rgb_image)
    save_image(msi_image)
    ocr_results = msi_ocr.read_text(msi_image.prepared_image)
    ocr_results = msi_ocr._remove_duplicates(ocr_results)

    assert len(ocr_results) == 2
    assert ocr_results[0].read_text == "Coolworking"
    assert ocr_results[1].read_text == "33000 Bordeaux"

'''
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
 ''' 


def create_fake_enveloppe(text:[]):
    fake_enveloppe = np.full((CAMERA_PREVIEW_HEIGHT, CAMERA_PREVIEW_WIDTH, 4), 255, dtype=np.uint8)
    y = CROPPED_IMAGE_TOP_LEFT_CORNER[1] 
    for line in text:
        size = cv2.getTextSize(line, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, thickness=2)
        width, height = size
        y += height * 3 + 5
        cv2.putText (img=fake_enveloppe, text=line, org=(CROPPED_IMAGE_TOP_LEFT_CORNER[0] + 10,  y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(0, 0, 255,100), thickness=2)     
    fake_enveloppe = cv2.cvtColor(fake_enveloppe, cv2.COLOR_BGR2RGB)
    return fake_enveloppe


def save_image(msi_image:MSIImage) -> None :
    if debug_mode:
        calling_function_name = (inspect.stack()[1][3]) 
        cv2.imwrite(temp_dir_path + f"/{calling_function_name}_rgb.jpg", msi_image.rgb_image)
        cv2.imwrite(temp_dir_path + f"/{calling_function_name}_prepared.jpg", msi_image.prepared_image) 
