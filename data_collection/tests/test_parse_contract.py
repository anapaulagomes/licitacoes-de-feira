import pytest
from data_collection.contracts.parse_contract import find_documents_and_names, parse_documents


def test_find_documents_and_names_contract1():
    sample = open(f'tests/contract_samples/contract1.txt')

    expected_data = {
        'name': 'MARIA SOLANGE MASCARENHAS RODRIGUES',
        'document': '13099647500',
        'legal_representant': 'MARIA SOLANGE MASCARENHAS RODRIGUES',
        'legal_representant_document': '13099647500'
    }
    assert find_documents_and_names(sample.read()) == expected_data


def test_find_documents_and_names_contract2():
    sample = open(f'tests/contract_samples/contract2.txt')

    expected_data = {
        'name': 'Luis Carlos dos Anjos Borges - ME',
        'document': '19924227000151',
        'legal_representant': 'Luis Carlos dos Anjos Borges',
        'legal_representant_document': '70775826553'
    }
    assert find_documents_and_names(sample.read()) == expected_data


def test_find_documents_and_names_contract3():
    sample = open(f'tests/contract_samples/contract3.txt')

    expected_data = {
        'name': 'M E B SERVICOX  E LOCACOES LTDA - ME',
        'document': '05824468000114',
        'legal_representant': 'DORANEIDE DOS REIS SOARES',
        'legal_representant_document': '48001708500'
    }
    assert find_documents_and_names(sample.read()) == expected_data


def test_find_documents_and_names_contract4():
    sample = open(f'tests/contract_samples/contract4.txt')

    expected_data = {
        'name': 'GGSC COMERCIO E SERVIÇOS EIRELI - ME',
        'document': '26218260000121',
        'legal_representant': 'Geny Gabrielly da Silva Cavalcanti',
        'legal_representant_document': '01462018205'
    }
    assert find_documents_and_names(sample.read()) == expected_data


def test_find_documents_and_names_contract5():
    sample = open(f'tests/contract_samples/contract5.txt')

    expected_data = {
        'name': 'MARIA SOLANGE MASCARENHAS RODRIGUES',
        'document': '13099647500',
        'legal_representant': 'MARIA SOLANGE MASCARENHAS RODRIGUES',
        'legal_representant_document': '13099647500'
    }
    assert find_documents_and_names(sample.read()) == expected_data


def test_find_documents_and_names_contract_with_symbol():
    sample = "PREFEITURA MUNICIPAL OE FEIRA DE SANTANA Secretaria Municipal de Administração Departamento de Licitação e Contratos CONTRATO RO 106 — 2017— WC Contrato que entre si de um lado, o MUNICÍPIO DE FEIRA DE SANTANA, jurídka de direito púdto interno, inwita no CNPJ sob o no 14.043.574/0001-51, com sede na Av. Senhor dos Pasos, no 980, Cmtro - Era de pelo Sr. José Ronaldo de Grva\'ho, autorizado art. 86, XIV, da sua Lei Orgânica, dorava denominado CONTRATANTE e, do outro lado, M E B SERVICO E LOCACOES LTDA - ME , estabelecida na Rua Barão dc Cotegipe, no 1 14, bairro, Centro, cidade Feira de Santana, inscrtã no CND sab no 05.824.468.0001-14 atrav& do seu representante le-ga!, Sr.(a) DORANE[DE DOS REIS SOARFS, innito no CPF sob o no 480.017.085-00, denomgnada CONTRATADA, observada a Licita*o no 037-2017, Pregão Prxendal na 032•2017, que regerá Lei Federal no. 10.520, de 17 de julho de 2002; Lei Municipal no. 2.593/05 de 07 de julho de 2005; Lei Estadual no. 9.433/05 de OI de março de 2005; Lei Federal no. 123, de 14 de dezembm de 2006; Decreto Municipal no. 7.583, de 05 de setembro de 2008; Lei F&al no. 8.666, de 21 de junho de 1993, com alteraÑe posteriores e dernals normas aptlcáveis à sp&ie, as c%usulas e CLÁUSULA PRIMEIRA - OBJETO CONTRATAÇÃO DE EMPRESA ESPECIALIZADA NA PRESTAÇÃO DE SEMÇO DE IMPRESSÕES E CÓPIAS REPROGRÁFICAS, PARA ATENDER AS NECESSIDADES DA SECRETARIA MUNICIPAL DE EDUCAÇÃO E DAS SCOLAS MUNICIPAIS, PELO PERÍODO DE 12 (DOZE) MESES. É v±da a subconratação parcial do objeto, a da com Ouüem, a ou tran±inda, total ou parchl do contrato, bem a fusão, dsão ou da antratada, não o por nenhum compromisso assumido por aquela cnrn terceiros. SIO. A CONTRATADA ficará obrigada a aczitar, nas conYatuais acrecimos ou suprsiE que fizerem no objeto, de do valor inicial atualizado do antraü), na forrna dos SIO e 3\' do art. 65 da Lei Federal no. 8.666/93. 520. As poderão ser superiore a 25%, dsde que haja resultado de acordo entre os mnb-abnt&. CLÁUSULA SEGUNDA — PRAZO O prazo de será de 12 (doze) mses, a partir da emisSo da primeira ordem de considerando o prazo de 24 e quatro) homs para a do *Niço, após ada solicitação. CLÁUSULA TERCEIRA - PREÇO O Contra-ante pagará à Contratada 0 de R$ e seis mil reais): VLR. AL cóPIAS E IMPRESSOS COLORIDAS NO TAMANHO A3 E IMPRESS 250 G, NO TAMANHO A3 2 SRV COLORJDAS PAPEL SRV E IMPRESS , NO TAMANHO Al SRV QTD 10.om 200 UNITÁRIO R$lm R$4Ñ0 2$10,00 -2017 R$IO.OM,OO R$24.OOO,m R$2.OOO,OO PREFEITURA MUNICIPAL OE FEIRA OE SANTANA Secretaria Municipal de Administração Departamento de Licitação e Contratos PLAS E IM , NO TAMANHO A2. SRV 4 6 7 REPROGRAFICAS E IMP MONOCROMÁTICAS NOS TAMANHOS A4 , CARTA OFÍCIO REPROG FICAS E IMP COLORIDAS NOS TAMANHOS A4,CARTA OU OFÍCIO 300 600.000 60.000 ENCARD SRV , MINIMO 50 FOLHAS, PAPEL A4, R$10,oo 2$0,15 R$2,OO R$1.90 R$3.ooo,oo R$120.OOOÑO R$57.OOO,w QUANTIDADE ESTIMADA PARA O PERIODO DE 12 SRV (DOZE) MESES VALOR TOTAL: VALOR POR EXTENSO: e seis mil reais SIO - Nos previstos Contrab incluídos todos os custos material de salários, encargos g)ciais, previdenciários e trabalhistas de todo o pe•al da CONTRATADA, como também fardanmto, transporte de qualquer natureza, materiais empregados, indusive ferramentas, e utilizados, depreciação, aluguéis, administração, impostos, taxas, emolumentos e quaisquer outros cuflos que, direta ou indiretamente, se relacionem 0 fiel Cumprimento pela CONTRATADA das oygações. QUARTA - DOTAÇÃO As para o pagamento deste contrato correrão por conta dos da Orçamentária a seguir 09 -/ SECRETARIA MUNICIP EDUChCÃO - SEDUC CLÁUSULA QUINTA - PAGAMENTO DE Projeb/A8v\"ade: 12.365.047.2037 12.361.047.2036 12.122.004.2032 Elemento de 33.9{139.99 Fonte 01 Os pagamentos devidos à efetuados através de ordem barrária ou crédito em conta após apresentação da Nota Fiscal/Fatura e entrega, devidamente atestada a execução conratual, não haja pend&\'cia a ser regularizada pelo conbatado. SIO. Em havendo alguma pend&-tcia in—tiva do pagamento, será considerada data da da fira aqueia na qual ocorreu a da por parte da CONTMTADA. 520. A atualização monetária dos pagarnentos devidos pela Administração, em de mora, será calculada considerando a data do vencimento da Nota fiscal/Fatura e do seu ±tivc pagamenb, de acordo com a variação do do IBGE pro raE tempore CLÁUSULA SEXTA - MANUTENÇÃO DAS CONDIÇÓES DA PROPOSTA —REAJUSTAMENTO E REVISÃO q são fixos e irreajustáveis. CLÁUSULA SÉTIMA - OBRIGAÇÓES DA CONTRATADA A CONTRATADA, além das determinações contuas ANEXO I do Edital e decorrentes de lei, obriga- a) prestar o objeto de acordo as constantes no de licitação e no contrato, ms tocais, dias e turnos determinados Adminisfração; b) zelar pela boa e compl*a contrato e por todos os rneios ao seu alcance, a ampla ação fscalizadora dos prem*os CONTRATANTE, ptontamente às e ue lhe forem solictadas;"
    expected_data = {
        'name': 'M E B SERVICO E LOCACOES LTDA - ME',
        'document': '05824468000114',
        'legal_representant': 'DORANEDE DOS REIS SOARFS',
        'legal_representant_document': '48001708500'
    }
    assert find_documents_and_names(sample) == expected_data


@pytest.mark.parametrize('document,expected_document', [
    ('013.876.645•22', '01387664522'),
    ('14.043.574]0001-51', '14043574000151'),
    ('02.921.456/0001-10', '02921456000110'),
    ('032.668.995- 80', '03266899580'),
    ('032.668.995- 80', '03266899580'),
])
def test_find_documents(document, expected_document):
    assert parse_documents(document)[0] == expected_document
