import os
import pandas as pd


DATA_DIRECTORY = "../data/payments/"
sheets = os.listdir(DATA_DIRECTORY)

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
all_payments = all_payments[to_be_striped].applymap(lambda value: str(value).strip())

all_payments.to_csv(path_or_buf=f"{DATA_DIRECTORY}all_payments.csv", index=False)
