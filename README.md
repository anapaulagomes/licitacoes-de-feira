# Licitações e Contratos de Feira

Uma ferramenta para facilitar o acesso as [licitações realizadas pela
prefeitura de Feira de
Santana](http://www.feiradesantana.ba.gov.br/servicos.asp?id=2&s=a&cat=PMFS&dt=01-2017&link=seadm/licitacoes.asp).
🏦

## Instalando

Para instalar as dependências você precisa de Python 3 em sua máquina. Execute:

```bash
pip install -r requirements.txt
```

Caso queira contribuir desenvolvendo, instale também as dependências de
desenvolvimento:

```bash
pip install -r requirements_dev.txt
```

## Hora da mágica

### Licitações

Para executar o crawler que busca as licitações:

```bash
scrapy runspider data_collection/bids/crawlers.py -o data_collection/data/bids/bids.json
```

### FrontEnd

Se quiser executar a aplicação:

```
cd frontend/
npm start
```
