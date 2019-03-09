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

[contratos-prefeitura-2016-2017.xls](http://www.transparencia.feiradesantana.ba.gov.br/index.php?view=contratos)

Fonte:
- http://www.transparencia.feiradesantana.ba.gov.br/index.php?view=contratos

[contracts-url-feira-de-santana-2016-2017.csv](https://github.com/anapaulagomes/licitacoes-de-feira/blob/master/data_collection/data/contracts/contracts-url-feira-de-santana-2016-2017.csv) (Obrigada, Turicas!)

### Sócios das Empresas Brasileiras

Coincidência ou não, boa parte dos contratos está preenchida com CNPJ/CPF errados.
Nesses contratos, foram encontrados 401 documentos únicos. 275 não encontrados.
Dos não encontrados, alguns tinham apenas o último dígito modificado.
Para encontrar os documentos, parseei o documento de assinatura do contrato.

## Comandos

### Baixando todos os PDFs do CSV de URLs

`wget -i data_collection/data/contracts/contracts-url-feira-de-santana-2016-2017.csv -P data_collection/data/contracts/pdfs/`
