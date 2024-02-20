
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
save_image_for_debugging = True 


def test_can_read_clean_image() :
    rgb_image = create_fake_enveloppe(["Coolworking", "9 rue de Conde", "33000 Bordeaux"])
    msi_image =  MSIImage(rgb_image)
    save_image(msi_image)
    ocr_results = msi_ocr.extract_text(msi_image.prepared_image)
    assert len(ocr_results) == 3
    assert ocr_results[0].read_text == "Coolworking"
    assert ocr_results[1].read_text == "9 rue de Conde"
    assert ocr_results[2].read_text == "33000 Bordeaux"


def test_can_filters_parasites() :
    rgb_image = create_fake_enveloppe(["Coolworking", ")    ."])
    msi_image =  MSIImage(rgb_image)
    save_image(msi_image)
    read_lines = msi_ocr.extract_text(msi_image.prepared_image)
    assert len(read_lines) == 1
    assert read_lines[0].read_text == "Coolworking"


def test_flags_duplicates_as_discarded():
    rgb_image = create_fake_enveloppe(["Coolworking", "Coolworking", "33000 Bordeaux"])
    msi_image =  MSIImage(rgb_image)
    save_image(msi_image)
    read_lines:list[OcrResult] = msi_ocr.extract_text(msi_image.prepared_image)
    msi_ocr._discard_duplicates(read_lines)
    
    assert len(read_lines) == 3
    assert read_lines[0].read_text == "Coolworking"
    assert not read_lines[0].is_discarded()
    assert read_lines[1].read_text == "Coolworking"
    assert read_lines[1].is_discarded()
    assert read_lines[2].read_text == "33000 Bordeaux"
    assert not read_lines[2].is_discarded()


def test_discards_non_relevant_words() :
    address = ["Recommande", "Fleur de vie", "9 rue de Conde", "33000 Bordeaux"]
    rgb_image = create_fake_enveloppe(address)
    msi_image =  MSIImage(rgb_image)
    save_image(msi_image)
    read_lines:list[OcrResult] = msi_ocr.extract_text(msi_image.prepared_image)
    msi_ocr._discard_non_relevant_lines(read_lines)
    assert len(read_lines) == 4
    assert read_lines[0].read_text == address[0]
    assert read_lines[0].is_discarded()
    assert read_lines[1].read_text == address[1]
    assert not read_lines[1].is_discarded()
    assert read_lines[2].read_text == address[2]
    assert read_lines[2].is_discarded()
    assert read_lines[3].read_text == address[3]
    assert read_lines[3].is_discarded()


def test_cleans_string_for_valid_lines ():
    address = ["Fabrice Jeannet", "Fleur de vie", "9 rue de Conde", "33000 Bordeaux"]
    rgb_image = create_fake_enveloppe(address)
    msi_image =  MSIImage(rgb_image)
    save_image(msi_image)
    read_lines:list[OcrResult] = msi_ocr.extract_text(msi_image.prepared_image)
    msi_ocr._discard_non_relevant_lines(read_lines)
   
    assert len(read_lines) == 4
   
    assert read_lines[0].read_text == address[0]
    assert not read_lines[0].is_discarded()
    assert read_lines[0].clean_text == "fabrice jeannet"

    assert read_lines[1].read_text == address[1]
    assert not read_lines[1].is_discarded()
    assert read_lines[1].clean_text == "fleur de vie"


    assert read_lines[2].read_text == address[2]
    assert read_lines[2].is_discarded()
    assert not read_lines[2].clean_text 

    assert read_lines[3].read_text == address[3]
    assert read_lines[3].is_discarded()
    assert not read_lines[3].clean_text 


def test_can_read_hyphen(): #depends mostly on confidence_threshold

    rgb_image = create_fake_enveloppe(["Test-hyphen"])
    msi_image =  MSIImage(rgb_image)
    save_image(msi_image)
    read_lines:list[OcrResult] = msi_ocr.extract_text(msi_image.prepared_image)
    assert len(read_lines) == 1
    assert read_lines[0].read_text == "Test-hyphen"

   
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


def create_fake_enveloppe(text:list[str]):
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
    if save_image_for_debugging:
        calling_function_name = (inspect.stack()[1][3]) 
        cv2.rectangle(msi_image.rgb_image, (CROPPED_IMAGE_TOP_LEFT_CORNER[0], CROPPED_IMAGE_TOP_LEFT_CORNER[1]), (CROPPED_IMAGE_BOTTOM_RIGHT_CORNER[0], CROPPED_IMAGE_BOTTOM_RIGHT_CORNER[1]), color=(0, 255, 0,100), thickness=2)

        cv2.imwrite(temp_dir_path + f"/{calling_function_name}_rgb.jpg", msi_image.rgb_image)
        cv2.imwrite(temp_dir_path + f"/{calling_function_name}_prepared.jpg", msi_image.prepared_image) 
    