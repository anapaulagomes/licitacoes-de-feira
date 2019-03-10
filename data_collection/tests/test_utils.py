from data_collection.contracts.utils import (
    make_cnpj_valid,
    make_cpf_valid,
    make_document_valid,
    fix_leading_zeros,
)
import pytest


@pytest.mark.parametrize(
    "cnpj,expected_result",
    [("40521585000100", "40521585000100"), ("74096231000180", "74096231000187")],
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
    ],
)
def test_make_document_valid(document, expected_result):
    assert make_document_valid(document) == expected_result


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
