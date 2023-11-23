from fuzzywuzzy import fuzz
from utils.config import ConfigImporter

config = ConfigImporter()


def test_name_matching() :
    min_ratio = config.data["thresholds"]["owner_name_matching_ratio"]
    assert fuzz.token_sort_ratio("fabrice jeannet", "jeannet fabrice") == 100
    assert fuzz.token_sort_ratio("fabrice nicolas jeannet", "jeannet fabrice") >= min_ratio
    assert fuzz.token_sort_ratio("fabrisse janet", "jeannet fabrice") >= min_ratio
    assert fuzz.token_sort_ratio("fabrice joinot", "jeannet fabrice") < min_ratio