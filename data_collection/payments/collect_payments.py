from datetime import date, timedelta
import requests
import string


URL = "http://www.transparencia.feiradesantana.ba.gov.br/Relatorio/RelDespesaExcel.php"
LETTERS = list(string.ascii_uppercase)
CATEGORIES = ["PAG", "LIQ", "EMP"]
previous_date = date(2010, 1, 1)  # '01/01/2010'
final_date = date(2019, 1, 1)


def download_payments(params):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(URL, data=params, headers=headers)
    filename = f"payments-{params['fase'].lower()}-{previous_date}-{next_date}-{letter.lower()}.xls"
    print(filename)
    open(f"../data/payments/{filename}", "wb").write(response.content)
    return response


while previous_date <= final_date:
    next_date = previous_date.replace(year=previous_date.year + 1)
    print(previous_date, final_date)

    params = {
        "data": f"{previous_date.strftime('%d/%m/%Y')} - {next_date.strftime('%d/%m/%Y')}",  # 13/03/2017 - 12/03/2018
        "parametro": "relatorio_despesa_alfa",
    }
    for category in CATEGORIES:
        params["fase"] = category

        for letter in LETTERS:
            params["recebeLetra"] = letter
            download_payments(params)

    previous_date = next_date
