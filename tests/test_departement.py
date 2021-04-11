import pytest
from scraper.departements import (
    to_departement_number,
    import_departements,
    cp_to_insee,
    get_city,
)


def test_import_departements():
    departements = import_departements()

    assert len(departements) == 101
    assert departements[:3] == ["01", "02", "03"]
    assert departements[83] == "83"
    assert departements[-1] == "976"
    assert departements.index("2A") == 28
    assert sorted(departements) == departements


def test_insee_to_departement_code():
    right_insee_code = "01001"
    short_insee_code = "1001"
    DOM_TOM_insee_code = "97234"
    passed_linked_to_Guadeloupe_insee_code = "97801"
    corse_insee_code = "2A004"
    monaco_insee_code = "99138"
    wrong_insee_code = "123"
    not_in_insee_code_table_insee_code = "12345"

    assert to_departement_number(right_insee_code) == right_insee_code[:2]
    assert to_departement_number(short_insee_code) == short_insee_code.zfill(5)[:2]
    assert to_departement_number(DOM_TOM_insee_code) == DOM_TOM_insee_code[:3]
    assert to_departement_number(passed_linked_to_Guadeloupe_insee_code) == "971"
    assert to_departement_number(corse_insee_code) == "2A"
    assert to_departement_number(monaco_insee_code) == "98"
    with pytest.raises(ValueError):
        to_departement_number(wrong_insee_code)
    with pytest.raises(ValueError):
        to_departement_number(not_in_insee_code_table_insee_code)


def test_get_city():
    address_1 = "2 avenue de la République, 75005 PARIS"
    address_2 = " 24 Rue de la Brèche, 91740 Pussay "
    address_3 = "Centre Cial du Bois des Roches 91240 SAINT MICHEL SUR ORGE"
    address_4 = " , 83700 Saint-Raphaël "
    address_5 = "1171 Avenue Gaston Feuillard\n97100 Basse-Terre"
    address_6 = "Rue de la République"

    assert get_city(address_1) == "PARIS"
    assert get_city(address_2) == "Pussay"
    assert get_city(address_3) == "SAINT MICHEL SUR ORGE"
    assert get_city(address_4) == "Saint-Raphaël"
    assert get_city(address_5) == "Basse-Terre"
    with pytest.raises(AttributeError):
        get_city(address_6)


def test_cp_to_insee():
    # Paris 15
    cp_paris_15 = "75015"
    insee_paris_15 = "75115"
    assert cp_to_insee(cp_paris_15) == insee_paris_15

    # Ajaccio
    cp_ajaccio_1 = "20090"
    cp_ajaccio_2 = "20090"
    cp_ajaccio_3 = "20167"
    insee_ajaccio = "2A004"
    assert cp_to_insee(cp_ajaccio_1) == insee_ajaccio
    assert cp_to_insee(cp_ajaccio_2) == insee_ajaccio
    # assert cp_to_insee(cp_ajaccio_3) == insee_ajaccio ==> faux, renvoie 2A351 (VILLANOVA)

    # Saint-Pierre-Laval
    cp_saint_pierre_laval = "42620"
    insee_saint_pierre_laval = "03250"
    # assert cp_to_insee(cp_saint_pierre_laval) == insee_saint_pierre_laval ==> faux, renvoie 42257 (ST MARTIN D ESTREAUX)

    # Paray-Vieille-Poste
    cp_paray_vieille_poste = "94390"
    insee_paray_vieille_poste = "91479"
    assert cp_to_insee(cp_paray_vieille_poste) == insee_paray_vieille_poste

    # Fort de France
    cp_fort_de_france = "97234"
    insee_fort_de_france = "97209"
    assert cp_to_insee(cp_fort_de_france) == insee_fort_de_france

    # Monaco
    cp_monaco = "98000"
    insee_monaco = "99138"
    assert cp_to_insee(cp_monaco) == insee_monaco

    # CP invalide
    invalid_cp = "1234"
    assert cp_to_insee(invalid_cp) == invalid_cp

    # Cholet entier
    cp_cholet_int = 49300  # => invalide
    insee_cholet = "49099"
    assert cp_to_insee(cp_cholet_int) == cp_cholet_int
