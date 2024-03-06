from utils.config import ConfigImporter
from enum import Enum

config = ConfigImporter()

#---------- CSV ----------
ID = config.data["csv_headers"]["id"]
STATUS = config.data["csv_headers"]["status"]
COMPANY_NAME = config.data["csv_headers"]["company_name"]
TRADEMARK = config.data["csv_headers"]["trademark"]
OWNER = config.data["csv_headers"]["owner"]
DOMICILIARY = config.data["csv_headers"]["domiciliary"]

SUBSCRIBED = config.data["subscription_statuses"]["abonne"]
UNSUBSCRIBED = config.data["subscription_statuses"]["desabonne"]
TERMINATED = config.data["subscription_statuses"]["radie"]

OWNER_MATCHING_THRESHOLD = config.data["thresholds"]["owner_name_matching_ratio"]

LEGAL_STATUSES = config.data["legal_statuses"]
NON_RELEVANT_STRINGS = config.data["non_relevant_strings"]
NON_RELEVANT_STRINGS_RATIO = config.data["thresholds"]["non_relevant_string_ratio"]

GENDER_MARKS = config.data["gender_marks"]

#---------- Camera ----------
CAMERA_PREVIEW_WIDTH = config.data["camera"]["preview_width"]
CAMERA_PREVIEW_HEIGHT = config.data["camera"]["preview_height"]
MOTION_DETECTION_THRESHOLD = config.data["camera"]["motion_detection_threshold"]
STEADY_TIMEOUT =  config.data["camera"]["steady_timeout"]


#---------- Image ----------
CROPPED_IMAGE_WIDTH = config.data["image"]["cropped_image_width"]
CROPPED_IMAGE_HEIGHT =  config.data["image"]["cropped_image_height"]
CROPPED_IMAGE_TOP_LEFT_CORNER = [int((CAMERA_PREVIEW_WIDTH - CROPPED_IMAGE_WIDTH)/2), int((CAMERA_PREVIEW_HEIGHT- CROPPED_IMAGE_HEIGHT)/2)]
CROPPED_IMAGE_BOTTOM_RIGHT_CORNER = [CROPPED_IMAGE_TOP_LEFT_CORNER[0] + CROPPED_IMAGE_WIDTH, CROPPED_IMAGE_TOP_LEFT_CORNER[1] + CROPPED_IMAGE_HEIGHT]
MEDIAN_BLUR_VALUE = config.data["image"]["median_blur_value"]


#---------- Events ----------
EVENTS = Enum("EVENTS", ["MOTION_DETECTED_EVENT", "CAMERA_STEADY_EVENT"])


#---------- PyTesseract ----------
LANGUAGE = config.data["pytesseract"]["language"]
CONFIDENCE_THRESHOLD = config.data["pytesseract"]["confidence_threshold"]

DIGIT_SEQUENCE = config.data["digit_sequence"]

LOGOS = config.data["logos"]