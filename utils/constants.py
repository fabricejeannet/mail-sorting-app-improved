from utils.config import ConfigImporter

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