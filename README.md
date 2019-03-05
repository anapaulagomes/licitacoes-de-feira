# Licitações de Feira

Uma ferramenta para facilitar o acesso as [licitações realizadas pela
prefeitura de Feira de Santana](http://www.feiradesantana.ba.gov.br/servicos.asp?id=2&s=a&cat=PMFS&dt=01-2017&link=seadm/licitacoes.asp). 🏦

## Hora da mágica

Para executar o crawler que busca as licitações:

`scrapy runspider data_collection/crawlers.py -o data_collection/data/bids.json`

Se quiser executar a aplicação:

```
cd frontend/
npm start
```
