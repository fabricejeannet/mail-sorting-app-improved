from utils.string_cleaner import StringCleaner

sc = StringCleaner()


def test_string_cleaner_removes_sas_legal_status() :
    assert sc.clean("sas Ma boîte totosas' sastoto SAS") == "ma boite totosas sastoto"


def test_string_cleaner_removes_sarl_legal_status() :
    assert sc.clean("sarl Ma boîte totosarl' sarltoto SARL") == "ma boite totosarl sarltoto"


def test_string_cleaner_removes_sarlu_legal_status() :
    assert sc.clean("sarlu Ma boîte totosarlu' sarlutoto SARLU") == "ma boite totosarlu sarlutoto"


def test_string_cleaner_removes_sarlu_legal_status() :
    assert sc.clean("sarlu Ma boîte totosarlu' sarlutoto SARLU") == "ma boite totosarlu sarlutoto"


def test_string_cleaner_removes_selarl_legal_status() :
    assert sc.clean("selarl Ma boîte totoselarl' selarltoto SELARL") == "ma boite totoselarl selarltoto"


def test_string_cleaner_removes_sasu_legal_status() :
    assert sc.clean("sasu Ma boîte totosasu' sasutoto SASU") == "ma boite totosasu sasutoto"


def test_string_cleaner_removes_eurl_legal_status() :
    assert sc.clean("eurl Ma boîte totoeurl' eurltoto EURL") == "ma boite totoeurl eurltoto"    


def test_string_cleaner_removes_sci_legal_status() :
    assert sc.clean("sci Ma boîte totosci' scitoto SCI") == "ma boite totosci scitoto"    


def test_string_cleaner_removes_snc_legal_status() :
    assert sc.clean("snc Ma boîte totosnc' snctoto SNC") == "ma boite totosnc snctoto"  


def test_string_cleaner_removes_ei_legal_status() :
    assert sc.clean("ei Ma boîte totoei' eitoto EI") == "ma boite totoei eitoto"     


def test_string_cleaner_removes_eirl_legal_status() :
    assert sc.clean("eirl Ma boîte totoeirl' eirltoto EIRL") == "ma boite totoeirl eirltoto"   


def test_is_not_a_relevant_word() :
    assert sc._is_not_a_relevant_string("33000 BORDEAUX") == True
    assert sc._is_not_a_relevant_string("33000 BORDEAUX") == True
    assert sc._is_not_a_relevant_string("33000 BOR") == True
    assert sc._is_not_a_relevant_string("par son representant") == True


def test_formatted_string_goes_to_lower_case():
    assert sc.format("MY STRING") == "my string"


def test_formatted_string_ends_are_trimmed():
    assert sc.format("  This String ") == "this string"


def test_formatted_string_has_no_accent():
    assert sc.format("ÂÊÎÔÛÄËÏÖÜÀÆæÇÉÈŒœÙ") == "aeiouaeiouaaeaeceeoeoeu"


def test_string_cleaner_replaces_amperstamp_with_et():
    assert sc.format("T&D") == "t et d"


def test_string_cleaner_remove_duplicated_white_spaces() :
    assert sc.format("too   many        whitespaces") == "too many whitespaces"


def test_string_cleaner_removes_all_non_words_chars() :
    assert sc.format("_no_more; non word chars:") == "no more non word chars"


def test_string_cleaner_removes_gender_marks():
    assert sc.format("monsieur jeannet madame meissner mme emma m. noah mlle tutu m lulu") == "jeannet meissner emma noah tutu lulu"
