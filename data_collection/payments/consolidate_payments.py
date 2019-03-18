from data_collection.utils import (
    add_mask_to_document,
    make_document_valid,
    functions_and_subfunctions_to_json,
)
import os
import pandas as pd
import re


DATA_DIRECTORY = "../data/payments/"
sheets = os.listdir(DATA_DIRECTORY)

modality_options = {
    "PREGAO": "PREGAO",
    "DISPENSA": "DISPENSA",
    "TOMADA DE PRECO": "TOMADA DE PRECO",
    "INEXIGIBILIDADE": "INEXIGIBILIDADE",
    "ISENTO": "ISENTO",
    "CONVITE": "CONVITE",
    "CONVENIO": "CONVENIO",
    "CONCORRENCIA": "CONCORRENCIA",
    "CONCURSO": "CONCURSO",
    "ONCORRENCIA": "CONCORRENCIA",
    "ISPENSA": "DISPENSA",
    "REGAO": "PREGAO",
    "NEXIGIBILIDADE": "INEXIGIBILIDADE",
    "SENTO": "ISENTO",
    "EGAO": "PREGAO",
    "EXIGIBILIDADE": "INEXIGIBILIDADE",
    "OMADA DE PRECO": "TOMADA DE PRECO",
    "SPENSA": "DISPENSA",
    "PENSA": "DISPENSA",
    "ENTO": "ISENTO",
    "NCORRENCIA": "CONCORRENCIA",
}

functions_and_subfunctions = functions_and_subfunctions_to_json(
    open("../data/functions_and_subfunctions.txt").read()
)


def normalize_modality(value):
    if modality_options.get(value.upper()):
        return modality_options.get(value.upper())
    return value.upper()


def normalize_cost(value):
    # from 69.848,70 (str) to 69848.70 (float)
    try:
        return float(value.replace(".", "").replace(",", "."))
    except ValueError as e:
        print(f"Something went wrong: {value}", e)
    return None


def normalize_function(value):
    if isinstance(value, str):
        code = re.sub("\D", "", value)
        if code:
            if functions_and_subfunctions.get(int(code)):
                return functions_and_subfunctions[int(code)]["label"]
        else:
            label = value.replace("-", "").strip()
            for func_details in functions_and_subfunctions.values():
                if label == func_details["label"]:
                    return label
                    break
    return "Inválido"


def normalize_document(value):
    # remove mask
    value = re.sub("\D", "", value)
    document = make_document_valid(value)
    return add_mask_to_document(document)


all_payments = pd.DataFrame()
for sheet in sheets:
    if ".xls" in sheet:
        try:
            payment = pd.read_excel(f"{DATA_DIRECTORY}{sheet}")
        except ImportError as e:
            print("Check your dependencies: ", e)
            break
        except Exception as e:
            # ignore if the file is empty
            if "File size is 0 bytes" in e.args[0]:
                print(f"File size is 0 bytes: {sheet}")
        else:
            all_payments = all_payments.append(payment, ignore_index=True)

# in portuguese in order to make it easier for whom is gonna use it
columns = {
    "Data de Publicacao": "data_de_publicacao",
    "Fase ": "fase",
    "Numero": "numero",
    "N do processo": "processo",
    "Bem / Servico Prestado": "bem_ou_servico_prestado",
    "Credor": "credor",
    "CPF / CNPJ": "cpf_ou_cnpj",
    "Valor": "valor",
    "Funcao": "funcao",
    "Subfuncao": "subfuncao",
    "Natureza": "natureza",
    "Fonte": "fonte",
    "Modalidade": "modalidade",
}
all_payments = all_payments.rename(index=str, columns=columns)

# remove extra spaces
to_be_striped = list(columns.values())
to_be_striped.remove("data_de_publicacao")
to_be_striped.remove("fase")
all_payments[to_be_striped] = all_payments[to_be_striped].applymap(
    lambda value: str(value).strip()
)

all_payments["modalidade"] = all_payments["modalidade"].apply(
    lambda value: normalize_modality(value)
)

all_payments["funcao"] = all_payments["funcao"].apply(
    lambda value: normalize_function(value)
)

all_payments["subfuncao"] = all_payments["subfuncao"].apply(
    lambda value: normalize_function(value)
)

all_payments["data_de_publicacao"] = pd.to_datetime(
    all_payments["data_de_publicacao"], format="%d/%m/%Y", errors="coerce"
)

all_payments["valor"] = all_payments["valor"].apply(lambda value: normalize_cost(value))

all_payments["cpf_ou_cnpj_corrigido"] = all_payments["cpf_ou_cnpj"].apply(
    lambda value: normalize_document(value)
)

all_payments.to_csv(path_or_buf=f"{DATA_DIRECTORY}all_payments.csv", index=False)
