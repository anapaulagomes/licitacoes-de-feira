# Coleta de dados

Aqui os scripts e dados relativos a [licitações](https://github.com/anapaulagomes/licitacoes-de-feira/tree/master/data_collection/bids) e [contratos](https://github.com/anapaulagomes/licitacoes-de-feira/tree/master/data_collection/contracts) do município
de Feira de Santana.

## Dados

### [Licitações](https://github.com/anapaulagomes/licitacoes-de-feira/tree/master/data_collection/data/bids)

Exemplo:

```
[{
    "id": 0,
    "url": "http://www.feiradesantana.ba.gov.br/seadm/licitacoes_pm.asp?cat=PMFS&dt=01-2019",
    "category": "PMFS",
    "month_year": "01-2019",
    "description": "Aquisi\u00e7\u00e3o de pneus, c\u00e2maras e protetores para atender a demanda dos ve\u00edculos das Secretarias Municipais de Administra\u00e7\u00e3o, Educa\u00e7\u00e3o e Desenvolvimento Social.(Horario Local)",
    "history": [
        {
            "when": "15/01/2019 15h18", 
            "event": "Resultado de impugna\u00e7\u00e3o", 
            "url": "http://www.feiradesantana.ba.gov.br/licitacoes/respostas/4413COMUNICADO_DE_IMPUGNA\u00c7\u00c3O__-_LIC.pdf"}
        ],
    "modality": "Licita\u00e7\u00e3o: 301-2018 / Preg\u00e3o Presencial: 171-2018",
    "when": "02/01/2019 08h30", 
    "document_url": "http://www.feiradesantana.ba.gov.br/licitacoes/4375pmfspp1712018.pdf"
}]
```

Fonte:
- http://www.feiradesantana.ba.gov.br/servicos.asp?id=2&s=a&cat=PMFS&dt=01-2017&link=seadm/licitacoes.asp

### [Contratos](https://github.com/anapaulagomes/licitacoes-de-feira/tree/master/data_collection/data/contracts)

Exemplo:

```
{
	"code": "651-2016-14C",
	"description": "AQUISI\u00c7\u00c3O DE MATERIAL DE CONSUMO PARA CASA DO TRABALHADOR CONV\u00caNIO 778827/2012 CONFORME OR\u00c7AMENTO EM ANEXO. PARA ENTREGA IMEDIATA EM AT\u00c9  05 DIAS LOCAL RUA CASTRO ALVES 894, CENTRO FEIRA DE SANTANA.O OR\u00c7AMENTO B\u00c1SICO FOI BASEADO PELA M\u00c9DIA DOS PRE",
	"start_date": "25/11/2016",
	"end_date": "25/11/2017",
	"cost": 7389.92,
	"contractor": {
		"name": "LIMP-AKY DISTRIBUIDORA LTDA - EPP",
		"document": "04702241000133",
		"document_type": "CNPJ",
		"sources": ["website-contracts", "parsed-contracts"],
		"data_from_pdf": {
			"documents": ["4702241000133"],
			"legal_representants": [{
				"name": "ANDERSON NOGUEIRA DUARTE",
				"document": "10440760623"
			}]
		}
	}
}
```

### Pagamentos

```
```

### Funções e subfunções

Fonte: http://www.tesouro.fazenda.gov.br/documents/10180/456785/Classifica%C3%A7%C3%A3o+Funcional.pdf/aa2723e7-850f-4098-9c4c-4e194f0f914c

Fonte:
- [contratos-prefeitura-2016-2017.xls](http://www.transparencia.feiradesantana.ba.gov.br/index.php?view=contratos)
- [contracts-url-feira-de-santana-2016-2017.csv](https://github.com/anapaulagomes/licitacoes-de-feira/blob/master/data_collection/data/contracts/contracts-url-feira-de-santana-2016-2017.csv) (Obrigada, Turicas!)

## Comandos

### Baixando todos os PDFs do CSV de URLs

`wget -i data_collection/data/contracts/contracts-url-feira-de-santana-2016-2017.csv -P data_collection/data/contracts/pdfs/`

### Extraindo documentos dos contratos (PDFs)

```
cd data_collection/
python contracts/parse_contract.py
```

Resultado: `data_collection/data/contracts/documents-from-contracts.csv`

### Consolidando os dados dos contratos

Coincidência ou não, boa parte dos contratos está preenchida com CNPJ/CPF errados.
Nesses contratos, foram encontrados 401 documentos únicos, sendo 216 inválidos
(e.g. dígitos verificadores diferentes, _leading zeros_ cortados pelo XLS).
Para encontrar os documentos corretos, foram utilizadas duas estratégias:

1. Calcular os dígitos verificadores
2. Extrair documentos dos contratos
3. Adicionar os zeros faltantes

```
cd data_collection/
python consolidate_contracts_info.py
```

Resultado: `data_collection/data/contracts/contracts.json`


### CSV para SQLite

```
rows csv2sqlite data/payments/all_payments.csv payments.sqlite
```