from data_collection.utils import (
    add_mask_to_document,
    make_cnpj_valid,
    make_cpf_valid,
    make_document_valid,
    fix_leading_zeros,
    functions_and_subfunctions_to_json,
)
import pytest


@pytest.mark.parametrize(
    "cnpj,expected_result",
    [
        ("40521585000100", "40521585000100"),
        ("74096231000180", "74096231000187"),
        ("13481460000120", "13481460000120"),  # a portinha
        ("00000000000191", "00000000000191"),  # banco do brasil
    ],
)
def test_make_cnpj_valid(cnpj, expected_result):
    assert make_cnpj_valid(cnpj) == expected_result


@pytest.mark.parametrize(
    "document,expected_result",
    [("11144477735", "11144477735"), ("25978004587", "25978004587")],
)
def test_make_cpf_valid(document, expected_result):
    assert make_cpf_valid(document) == expected_result


@pytest.mark.parametrize(
    "document,expected_result",
    [
        ("11144477735", "11144477735"),
        ("25978004587", "25978004587"),
        ("74096231000180", "74096231000187"),
        (None, None),
        ("910", "00000000949"),  # fix leading zeros
    ],
)
def test_make_document_valid(document, expected_result):
    assert make_document_valid(document) == expected_result


@pytest.mark.parametrize(
    "document,expected_result",
    [("44421109568", "444.211.095-68"), ("13481460000120", "13.481.460/0001-20")],
)
def test_add_mask_to_document(document, expected_result):
    assert add_mask_to_document(document) == expected_result


@pytest.mark.parametrize(
    "document,expected_result",
    [
        pytest.param("5868777000196", "05868777000196", id="cnpj missing one zero"),
        pytest.param("878183000142", "00878183000142", id="cnpj missing two zeros"),
        pytest.param("5838479515", "05838479515", id="cpf missing one zero"),
        pytest.param("653418566", "00653418566", id="cpf missing two zeros"),
        pytest.param("11334909000100", "11334909000100", id="valid cnpj"),
        pytest.param("13099647500", "13099647500", id="valid cpf"),
    ],
)
def test_fix_leading_zeros(document, expected_result):
    assert fix_leading_zeros(document) == expected_result


def test_convert_functions_txt_into_json():
    content = """01 - Legislativa
    031 - Ação Legislativa
    032 - Controle Externo
    02 - Judiciária
    061 - Ação Judiciária
    062 - Defesa do Interesse Público no Processo Judiciário
    99
    997 - Reserva do RPPS
    999 - Reserva de Contingência"""

    expected = {
        1: {"label": "Legislativa", "function": None},
        31: {"label": "Ação Legislativa", "function": 1},
        32: {"label": "Controle Externo", "function": 1},
        2: {"label": "Judiciária", "function": None},
        61: {"label": "Ação Judiciária", "function": 2},
        62: {
            "label": "Defesa do Interesse Público no Processo Judiciário",
            "function": 2,
        },
        99: {"label": None, "function": None},
        997: {"label": "Reserva do RPPS", "function": 99},
        999: {"label": "Reserva de Contingência", "function": 99},
    }

    assert functions_and_subfunctions_to_json(content) == expected
