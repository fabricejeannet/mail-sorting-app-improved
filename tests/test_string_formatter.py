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


def test_string_formatter_removes_sas_legal_status() :
    sf = StringFormatter()
    assert sf.format("sas Ma boîte totosas' sastoto SAS") == "ma boite totosas sastoto"


def test_string_formatter_removes_sarl_legal_status() :
    sf = StringFormatter()
    assert sf.format("sarl Ma boîte totosarl' sarltoto SARL") == "ma boite totosarl sarltoto"


def test_string_formatter_removes_sarlu_legal_status() :
    sf = StringFormatter()
    assert sf.format("sarlu Ma boîte totosarlu' sarlutoto SARLU") == "ma boite totosarlu sarlutoto"


def test_string_formatter_removes_sarlu_legal_status() :
    sf = StringFormatter()
    assert sf.format("sarlu Ma boîte totosarlu' sarlutoto SARLU") == "ma boite totosarlu sarlutoto"


def test_string_formatter_removes_selarl_legal_status() :
    sf = StringFormatter()
    assert sf.format("selarl Ma boîte totoselarl' selarltoto SELARL") == "ma boite totoselarl selarltoto"


def test_string_formatter_removes_sasu_legal_status() :
    sf = StringFormatter()
    assert sf.format("sasu Ma boîte totosasu' sasutoto SASU") == "ma boite totosasu sasutoto"


def test_string_formatter_removes_eurl_legal_status() :
    sf = StringFormatter()
    assert sf.format("eurl Ma boîte totoeurl' eurltoto EURL") == "ma boite totoeurl eurltoto"    


def test_string_formatter_removes_sci_legal_status() :
    sf = StringFormatter()
    assert sf.format("sci Ma boîte totosci' scitoto SCI") == "ma boite totosci scitoto"    


def test_string_formatter_removes_snc_legal_status() :
    sf = StringFormatter()
    assert sf.format("snc Ma boîte totosnc' snctoto SNC") == "ma boite totosnc snctoto"  


def test_string_formatter_removes_ei_legal_status() :
    sf = StringFormatter()
    assert sf.format("ei Ma boîte totoei' eitoto EI") == "ma boite totoei eitoto"     


def test_string_formatter_removes_eirl_legal_status() :
    sf = StringFormatter()
    assert sf.format("eirl Ma boîte totoeirl' eirltoto EIRL") == "ma boite totoeirl eirltoto"   