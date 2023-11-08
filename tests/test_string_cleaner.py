from utils.string_cleaner import StringCleaner


def test_string_formatter_removes_sas_legal_status() :
    sc = StringCleaner()
    assert sc.clean("sas Ma boîte totosas' sastoto SAS") == "ma boite totosas sastoto"


def test_string_formatter_removes_sarl_legal_status() :
    sc = StringCleaner()
    assert sc.clean("sarl Ma boîte totosarl' sarltoto SARL") == "ma boite totosarl sarltoto"


def test_string_formatter_removes_sarlu_legal_status() :
    sc = StringCleaner()
    assert sc.clean("sarlu Ma boîte totosarlu' sarlutoto SARLU") == "ma boite totosarlu sarlutoto"


def test_string_formatter_removes_sarlu_legal_status() :
    sc = StringCleaner()
    assert sc.clean("sarlu Ma boîte totosarlu' sarlutoto SARLU") == "ma boite totosarlu sarlutoto"


def test_string_formatter_removes_selarl_legal_status() :
    sc = StringCleaner()
    assert sc.clean("selarl Ma boîte totoselarl' selarltoto SELARL") == "ma boite totoselarl selarltoto"


def test_string_formatter_removes_sasu_legal_status() :
    sc = StringCleaner()
    assert sc.clean("sasu Ma boîte totosasu' sasutoto SASU") == "ma boite totosasu sasutoto"


def test_string_formatter_removes_eurl_legal_status() :
    sc = StringCleaner()
    assert sc.clean("eurl Ma boîte totoeurl' eurltoto EURL") == "ma boite totoeurl eurltoto"    


def test_string_formatter_removes_sci_legal_status() :
    sc = StringCleaner()
    assert sc.clean("sci Ma boîte totosci' scitoto SCI") == "ma boite totosci scitoto"    


def test_string_formatter_removes_snc_legal_status() :
    sc = StringCleaner()
    assert sc.clean("snc Ma boîte totosnc' snctoto SNC") == "ma boite totosnc snctoto"  


def test_string_formatter_removes_ei_legal_status() :
    sc = StringCleaner()
    assert sc.clean("ei Ma boîte totoei' eitoto EI") == "ma boite totoei eitoto"     


def test_string_formatter_removes_eirl_legal_status() :
    sc = StringCleaner()
    assert sc.clean("eirl Ma boîte totoeirl' eirltoto EIRL") == "ma boite totoeirl eirltoto"   


def test_is_not_a_relevant_word() :
    sc = StringCleaner()
    assert sc._is_not_a_relevant_string("33000 Bordeaux") == True
    assert sc._is_not_a_relevant_string("33000 Bordeau") == True
    assert sc._is_not_a_relevant_string("33000 Borde") == True
    assert sc._is_not_a_relevant_string("par son representant") == True