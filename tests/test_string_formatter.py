from utils.string_formatter import StringFormatter


def test_formatted_string_goes_to_lower_case():
    sf = StringFormatter()
    assert sf.format("MY STRING") == "my string"


def test_formatted_string_ends_are_trimmed():
    sf = StringFormatter()
    assert sf.format("  This String ") == "this string"


def test_formatted_string_has_no_accent():
    sf = StringFormatter()
    assert sf.format("ÂÊÎÔÛÄËÏÖÜÀÆæÇÉÈŒœÙ") == "aeiouaeiouaaeaeceeoeoeu"


def test_string_formatter_replaces_amperstamp_with_et():
    sf = StringFormatter()
    assert sf.format("T&D") == "t et d"


def test_string_formatter_remove_duplicated_white_spaces() :
    sf = StringFormatter()
    assert sf.format("too   many        whitespaces") == "too many whitespaces"


def test_string_formatter_removes_all_non_words_chars() :
    sf = StringFormatter()
    assert sf.format("_no_more; non word chars:") == "no more non word chars"