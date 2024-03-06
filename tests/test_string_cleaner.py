from utils.string_cleaner import StringCleaner

sc = StringCleaner()

def test_string_cleaner_remove_duplicated_white_spaces() :
    assert sc._remove_unnecessary_whitespaces(" too   many        whitespaces ") == "too many whitespaces"


def test_string_cleaner_removes_sas_legal_status() :
    given_string = "sas Ma boîte totosas' S.A.S. sastoto SAS"
    string_without_legal_statuses = sc._remove_legal_statuses(given_string)
    string_without_legal_statuses = sc._remove_unnecessary_whitespaces(string_without_legal_statuses)
    assert  string_without_legal_statuses == "Ma boîte totosas' sastoto"


def test_string_cleaner_removes_sarl_legal_status() :
    given_string = "sarl Ma boîte S.A.R.L. totosarl' sarltoto SARL"
    string_without_legal_statuses = sc._remove_legal_statuses(given_string)
    string_without_legal_statuses = sc._remove_unnecessary_whitespaces(string_without_legal_statuses)
    assert  string_without_legal_statuses == "Ma boîte totosarl' sarltoto"


def test_string_cleaner_removes_sarlu_legal_status() :
    given_string = "sarlu Ma boîte S.A.R.L.U. totosarlu' sarlutoto SARLU"
    string_without_legal_statuses = sc._remove_legal_statuses(given_string)
    string_without_legal_statuses = sc._remove_unnecessary_whitespaces(string_without_legal_statuses)
    assert  string_without_legal_statuses == "Ma boîte totosarlu' sarlutoto"


def test_string_cleaner_removes_selarl_legal_status() :
    given_string = "selarl Ma boîte S.E.L.A.R.L. totoselarl' selarltoto SELARL"
    string_without_legal_statuses = sc._remove_legal_statuses(given_string)
    string_without_legal_statuses = sc._remove_unnecessary_whitespaces(string_without_legal_statuses)
    assert  string_without_legal_statuses == "Ma boîte totoselarl' selarltoto"


def test_string_cleaner_removes_sasu_legal_status() :
    given_string = "sasu Ma boîte totosasu' S.A.S.U. sasutoto SASU"
    string_without_legal_statuses = sc._remove_legal_statuses(given_string)
    string_without_legal_statuses = sc._remove_unnecessary_whitespaces(string_without_legal_statuses)
    assert  string_without_legal_statuses == "Ma boîte totosasu' sasutoto"


def test_string_cleaner_removes_eurl_legal_status() :
    given_string = "eurl Ma boîte E.U.R.L. totoeurl' eurltoto EURL"
    string_without_legal_statuses = sc._remove_legal_statuses(given_string)
    string_without_legal_statuses = sc._remove_unnecessary_whitespaces(string_without_legal_statuses)
    assert  string_without_legal_statuses == "Ma boîte totoeurl' eurltoto"


def test_string_cleaner_removes_sci_legal_status() :
    given_string = "sci Ma boîte totosci' S.C.I. scitoto SCI"
    string_without_legal_statuses = sc._remove_legal_statuses(given_string)
    string_without_legal_statuses = sc._remove_unnecessary_whitespaces(string_without_legal_statuses)
    assert  string_without_legal_statuses == "Ma boîte totosci' scitoto"


def test_string_cleaner_removes_snc_legal_status() :
    given_string = "snc Ma boîte totosnc' S.N.C. snctoto SNC"
    string_without_legal_statuses = sc._remove_legal_statuses(given_string)
    string_without_legal_statuses = sc._remove_unnecessary_whitespaces(string_without_legal_statuses)
    assert  string_without_legal_statuses == "Ma boîte totosnc' snctoto"


def test_string_cleaner_removes_ei_legal_status() :
    given_string = "ei Ma boîte totoei' E.I. eitoto EI"
    string_without_legal_statuses = sc._remove_legal_statuses(given_string)
    string_without_legal_statuses = sc._remove_unnecessary_whitespaces(string_without_legal_statuses)
    assert  string_without_legal_statuses == "Ma boîte totoei' eitoto"


def test_string_cleaner_removes_eirl_legal_status() :
    given_string = "eirl Ma boîte E.I.R.L. totoeirl' eirltoto EIRL"
    string_without_legal_statuses = sc._remove_legal_statuses(given_string)
    string_without_legal_statuses = sc._remove_unnecessary_whitespaces(string_without_legal_statuses)
    assert  string_without_legal_statuses == "Ma boîte totoeirl' eirltoto"


def test_is_not_a_relevant_word() :
    assert sc._is_not_a_relevant_string("33000 BORDEAUX") == True
    assert sc._is_not_a_relevant_string("33000 BORDEAUX") == True
    assert sc._is_not_a_relevant_string("33000 BOR") == True
    assert sc._is_not_a_relevant_string("par son representant") == True
    assert sc._is_not_a_relevant_string("DI-20240301") == True
    assert sc._is_not_a_relevant_string("DI 20240301") == True
    assert sc._is_not_a_relevant_string("20240301") == True
    assert sc._is_not_a_relevant_string("DI 2024-0301") == True
    assert sc._is_not_a_relevant_string("2024-0301") == True

def test_string_cleaner_replaces_amperstamp_with_et():
    assert sc._replace_amperstamp_with_et("T&D") == "T et D"


def test_removes_special_characters_except_semicolon():
    assert sc._remove_special_characters_except_semicolon("first_word;second!word") == "first word;second word"


def test_formatted_string_has_no_accent():
    assert sc._remove_accents("ÂÊÎÔÛÄËÏÖÜÀÆÇÉÈŒÙ âêîôûäëïöüàæçéèœù") == "AEIOUAEIOUAAECEEOEU aeiouaeiouaaeceeoeu"


def test_string_cleaner_removes_all_non_words_chars() :

    clean_string = sc._remove_special_characters("_no_more; non word chars:!-()")
    clean_string = sc._remove_unnecessary_whitespaces(clean_string)
    assert clean_string == "no more non word chars"



def test_removes_gender_marks():
    clean_string = sc._remove_gender_marks("monsieur jeannet madame meissner mme emma m. noah mlle tutu m lulu mle lili")
    clean_string = sc._remove_unnecessary_whitespaces(clean_string)
    assert clean_string == "jeannet meissner emma noah tutu lulu lili"


def test_formatted_string_goes_to_lower_case():
    assert sc.format("MY STRING") == "my string"


def test_formatted_string_ends_are_trimmed():
    assert sc.format("  This String ") == "this string"

def test_clean_cosy_wine():
    assert sc.clean("S.A.S. Cosywine") == "cosywine"


def test_postal_digit_sequence_is_non_relevant():
    assert sc._is_a_postal_digit_sequence("DI-20240301") == True
    assert sc._is_a_postal_digit_sequence("DI 20240301") == True
    assert sc._is_a_postal_digit_sequence("20240301") == True
    assert sc._is_a_postal_digit_sequence("DI 2024-0301") == True
    assert sc._is_a_postal_digit_sequence("2024-0301") == True