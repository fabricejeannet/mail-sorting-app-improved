from utils.config import ConfigImporter
from enum import Enum

config = ConfigImporter()

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

RECTANGLE_START_POINT = (config.data["image"]["RECTANGLE_START_POINT"][0], config.data["image"]["RECTANGLE_START_POINT"][1])
RECTANGLE_END_POINT = (config.data["image"]["RECTANGLE_END_POINT"][0], config.data["image"]["RECTANGLE_END_POINT"][1])
RESIZED_IMAGE_WIDTH = config.data["image"]["RESIZED_IMAGE_WIDTH"]
RESIZED_IMAGE_HEIGHT =  config.data["image"]["RESIZED_IMAGE_HEIGHT"]
STEADY_WAIT_TIME =  config.data["image"]["STEADY_WAIT_TIME"]

EVENTS = Enum("EVENTS", ["MOTION_DETECTED_EVENT", "CAMERA_STEADY_EVENT"])

MOTION_DETECTION_THRESHOLD = config.data["camera"]["MOTION_DETECTION_THRESHOLD"]