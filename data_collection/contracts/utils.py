"""
Explanation (pt-br):
https://www.geradorcnpj.com/algoritmo_do_cnpj.htm
https://www.geradorcpf.com/algoritmo_do_cpf.htm
"""


def _calculate_verifier_digit(weigths, digits):
    result = []
    for digit, weight in zip(digits, weigths):
        result.append(digit * weight)

    magic_number = 11

    result_sum = sum(result)
    quotient = result_sum // magic_number
    rest = result_sum % magic_number

    if rest >= 2:
        return magic_number - rest
    return 0


def _make_document_valid(document, limit, first_weigth, second_weigth):
    original_first = document[-2]
    original_second = document[-1]

    digits = [int(digit) for digit in document[:limit]]

    first = _calculate_verifier_digit(first_weigth, digits)
    digits.append(first)

    second = _calculate_verifier_digit(second_weigth, digits)
    return f"{document[:limit]}{first}{second}"


def make_cnpj_valid(document):
    limit = 12
    first_weigth = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    second_weigth = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    return _make_document_valid(document, limit, first_weigth, second_weigth)


def make_cpf_valid(document):
    limit = 9
    first_weigth = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    second_weigth = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]

    return _make_document_valid(document, limit, first_weigth, second_weigth)


def make_document_valid(document):
    document = fix_leading_zeros(document)
    if len(document) == 11:
        return make_cpf_valid(document)
    elif len(document) == 14:
        return make_cnpj_valid(document)
    return document


def fix_leading_zeros(document):
    cnpj_len = 14
    cpf_len = 11
    doc_len = len(document)
    if doc_len == cnpj_len or doc_len == cpf_len:
        return document
    if cpf_len < doc_len < cnpj_len:
        return "0" * (cnpj_len - doc_len) + document
    if doc_len < cpf_len:
        return "0" * (cpf_len - doc_len) + document
