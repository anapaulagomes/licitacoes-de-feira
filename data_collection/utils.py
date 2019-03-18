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


def make_document_valid(value):
    if value is None:
        return value
    document = fix_leading_zeros(value)

    if len(document) == 11:
        return make_cpf_valid(document)
    elif len(document) == 14:
        return make_cnpj_valid(document)
    return document


def add_mask_to_document(document):
    if len(document) == 11:
        return f"{document[0:3]}.{document[3:6]}.{document[6:9]}-{document[-2:]}"
    elif len(document) == 14:
        # 13.481.460/0001-20
        return f"{document[0:2]}.{document[2:5]}.{document[5:8]}/{document[8:12]}-{document[-2:]}"
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


def functions_and_subfunctions_to_json(content):
    """
    Content copied from:
    http://www.tesouro.fazenda.gov.br/documents/10180/456785/Classifica%C3%A7%C3%A3o+Funcional.pdf/aa2723e7-850f-4098-9c4c-4e194f0f914c
    
    Format:
    01 - Legislativa
    031 - Ação Legislativa
    032 - Controle Externo
    02 - Judiciária

    To:
    expected: {
        1: {"label": "Legislativa", "function": None},
        31: {"label": "Ação Legislativa", "function": 1},
        32: {"label": "Ação Legislativa", "function": 1},
        2: {"label": "Judiciária", "function": None},
    }
    """
    divider = " - "
    functions_and_sub_functions = {}
    previous_function = None
    for line in content.splitlines():
        splited_line = line.strip().split(divider)
        code = str(splited_line[0])
        label = None
        if len(splited_line) == 2:
            label = splited_line[1]

        if len(code) > 2:
            code = int(code)
            functions_and_sub_functions[code] = {
                "label": label,
                "function": previous_function,
            }
        else:
            code = int(code)
            functions_and_sub_functions[code] = {"label": label, "function": None}
            previous_function = code
    return functions_and_sub_functions
