import os
import pandas as pd


DATA_DIRECTORY = "../data/payments/"
sheets = os.listdir(DATA_DIRECTORY)

values_key = {
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


def normalize_modality(value):
    if values_key.get(value.upper()):
        return values_key.get(value.upper())
    return value.upper()


def normalize_cost(value):
    # 69.848,70
    try:
        return float(value.replace(".", "").replace(",", "."))
    except ValueError as e:
        print(f"Something went wrong: {value}", e)
    return None


all_payments = pd.DataFrame()
for sheet in sheets:
    try:
        payment = pd.read_excel(f"{DATA_DIRECTORY}{sheet}")
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

all_payments["data_de_publicacao"] = pd.to_datetime(
    all_payments["data_de_publicacao"], format="%d/%m/%Y", errors="coerce"
)

all_payments["valor"] = all_payments["valor"].apply(lambda value: normalize_cost(value))

all_payments.to_csv(path_or_buf=f"{DATA_DIRECTORY}all_payments.csv", index=False)
