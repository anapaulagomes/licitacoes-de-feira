import pytest
from data_collection.contracts.parse_contract import find_documents_and_names


def test_find_documents_and_names_contract1():
    sample = open(f'tests/contract_samples/contract1.txt')

    expected_data = {
        'name': 'MARIA SOLANGE MASCARENHAS RODRIGUES',
        'document': '13099647500',
        'legal_representant': 'MARIA SOLANGE MASCARENHAS RODRIGUES',
        'legal_representant_document': '13099647500'
    }
    assert find_documents_and_names(sample.read()) == expected_data


def test_find_documents_and_names_contract2():
    sample = open(f'tests/contract_samples/contract2.txt')

    expected_data = {
        'name': 'Luis Carlos dos Anjos Borges - ME',
        'document': '19924227000151',
        'legal_representant': 'Luis Carlos dos Anjos Borges',
        'legal_representant_document': '70775826553'
    }
    assert find_documents_and_names(sample.read()) == expected_data


def test_find_documents_and_names_contract3():
    sample = open(f'tests/contract_samples/contract3.txt')

    expected_data = {
        'name': 'M E B SERVICOX  E LOCACOES LTDA - ME',
        'document': '05824468000114',
        'legal_representant': 'DORANEIDE DOS REIS SOARES',
        'legal_representant_document': '48001708500'
    }
    assert find_documents_and_names(sample.read()) == expected_data


def test_find_documents_and_names_contract4():
    sample = open(f'tests/contract_samples/contract4.txt')

    expected_data = {
        'name': 'GGSC COMERCIO E SERVIÇOS EIRELI - ME',
        'document': '26218260000121',
        'legal_representant': 'Geny Gabrielly da Silva Cavalcanti',
        'legal_representant_document': '01462018205'
    }
    assert find_documents_and_names(sample.read()) == expected_data


def test_find_documents_and_names_contract5():
    sample = open(f'tests/contract_samples/contract5.txt')

    expected_data = {
        'name': 'MARIA SOLANGE MASCARENHAS RODRIGUES',
        'document': '13099647500',
        'legal_representant': 'MARIA SOLANGE MASCARENHAS RODRIGUES',
        'legal_representant_document': '13099647500'
    }
    assert find_documents_and_names(sample.read()) == expected_data
