from data_collection.contracts.utils import make_cnpj_valid, make_cpf_valid, make_document_valid
import pytest


@pytest.mark.parametrize('cnpj,expected_result', [
    ('40521585000100', '40521585000100'),
    ('74096231000180', '74096231000187'),
])
def test_make_cnpj_valid(cnpj, expected_result):
    assert make_cnpj_valid(cnpj) == expected_result


@pytest.mark.parametrize('document,expected_result', [
    ('11144477735', '11144477735'),
    ('25978004587', '25978004587'),
])
def test_make_cpf_valid(document, expected_result):
    assert make_cpf_valid(document) == expected_result


@pytest.mark.parametrize('document,expected_result', [
    ('11144477735', '11144477735'),
    ('25978004587', '25978004587'),
    ('74096231000180', '74096231000187'),
    ('1', '1'),
])
def test_make_document_valid(document,expected_result):
    assert make_document_valid(document) == expected_result
