import requests

"""
Source: http://www.tcm.ba.gov.br/portal-da-cidadania/pessoal/
?tipo=xls&entidades=129&ano=2017&mes=1&tipoRegime=1&receitaLiquidaMensal=0,00
&receitaLiquidaAte=0,00&receitaLiquidaPeriodo="Janeiro de 2016 até Janeiro de 2017"
"""
entities = {
    129: {"name": "Prefeitura Municipal de FEIRA DE SANTANA", "slug": "city-hall"},
    544: {"name": "Camara Municipal de FEIRA DE SANTANA", "slug": "concilman"},
    880: {
        "name": "Instituto de Previdência de Feira de Santana",
        "slug": "pension-institute",
    },
    892: {
        "name": "Fundação Hospitalar de Feira de Santana",
        "slug": "hospital-foundation",
    },
    984: {
        "name": "Superintendência Municipal de Trânsito",
        "slug": "superintendence-of-traffic",
    },
    1008: {
        "name": "Fundação Cultural Municipal Egberto Tavares Costa",
        "slug": "egberto-tavares-costa",
    },
    1032: {
        "name": "Superintendência Municipal de Proteção e Defesa do Consumidor",
        "slug": "procon",
    },
    1033: {"name": "Agência Reguladora de Feira de Santana", "slug": "arfes"},
    1104: {
        "name": "Consórcio Público Interfederativo De Saúde Da Região de Feira de Santana",
        "slug": "portal-do-sertao",
    },
}

months = range(1, 13)
years = [2016, 2017]

for year in years:
    for month in months:
        for entity_id, entity_data in entities.items():
            params = {
                "tipo": "xls",
                "entidades": entity_id,
                "ano": year,
                "mes": month,
                "tipoRegime": 1,  # all of them
                "receitaLiquidaMensal": "0,00",  # from this point, only required and useless fields
                "receitaLiquidaAte": "0,00",
                "receitaLiquidaPeriodo": "Janeiro de 2016 até Janeiro de 2017",
            }

            print(f"{year}-{month}-{entity_data['slug']}")

            response = requests.post(
                "https://www.tcm.ba.gov.br/Webservice/index.php/exportar/pessoal",
                allow_redirects=True,
                params=params,
            )
            open(
                f"../data/people/people-feira-{year}-{month}-{entity_data['slug']}.xls",
                "wb",
            ).write(response.content)
