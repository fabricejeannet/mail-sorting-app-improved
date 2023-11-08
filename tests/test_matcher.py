from domain.matcher import Matcher


df = pd.read_csv("test.csv")
matcher = Matcher(df)

def test_returns_a_100_percent_matching_company_name_tuple():
    tuple = matcher.get("Bordeaux Rénov")
    assert len(tuple) == 1
