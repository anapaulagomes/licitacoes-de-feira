import os
import re
import requests
import requests_cache
from io import StringIO


ONE_DAY_IN_SECONDS = 86400
CNPJ_PATTERN = re.compile(r'\d{2}\.\d{3}\.\d{3}[\/|.]\d{4}-\d{2}')
CPF_PATTERN = re.compile(r'\d{3}\.\d{3}\.\d{3}-\d{2}')
CNPJ_OR_CPF_PATTERN = re.compile(r'\d{2}\S+\d{3}\S+\d{3}\S+\d{4}.*?\d{2}|\d{3}\S+\d{3}\S+\d{3}.*?\d{2}')
CONTRACT_HEADER_PATTERN = re.compile(r'do outro lado,(.*) |cláusulas e condições seguintes')
LEGAL_REPRESENTANT_PATTERN = re.compile(r'representante .+? (.+?),')

requests_cache.install_cache(cache_name='contracts/ocrspace_cache', backend='sqlite', expire_after=ONE_DAY_IN_SECONDS)


def clean_document(string):
    string = re.sub(r'[^\w]', ' ', string)
    string = string.replace(' ', '')
    return string.lstrip().rstrip()

def clean_string(string):
    words = string.split(' ')
    # removing symbols in the middle of the name
    for word in words:
        string = re.sub(r'[^\w]', ' ', string)
    return ' '.join([
        re.sub(r'[^\w]', ' ', word).replace(' ', '')
        for word in words
    ])


def parse_name(header):
    index_name = header.find(',')
    name = header[:index_name]
    return name.lstrip().rstrip()


def parse_legal_representant(header):
    salutations = ['Sr ', 'Sra ', 'Sr,(a) ', 'Sr. ', 'Sr.(a) ']
    for salutation in salutations:
        if salutation in header:
            header = header.replace(salutation, '')
    legal_representant = re.findall(LEGAL_REPRESENTANT_PATTERN, header)
    if legal_representant != []:
        return clean_string(legal_representant[0])
    return ''


def parse_documents(header):
    documents = re.findall(CNPJ_OR_CPF_PATTERN, header)
    if documents:
        return [
            clean_document(document)
            for document in documents
        ]
    return []


def find_documents_and_names(sample):
    header = re.findall(CONTRACT_HEADER_PATTERN, sample)
    if header:
        header = header[0]
        name = parse_name(header)

        index_name = header.find(name)
        header_without_name = header[index_name:]
        
        legal_representant = parse_legal_representant(header_without_name)
        documents = parse_documents(header)
        document = None
        legal_representant_document = None
        if documents:
            document = documents[0]
            try:
                legal_representant_document = documents[1]
            except:
                pass

        return {
            'name': name,
            'document': document,
            'legal_representant': legal_representant,
            'legal_representant_document': legal_representant_document
        }
    return {}


def retrieve_content_from_pdf(pdf_url):
    """
    API: https://ocr.space/ocrapi
    """
    payload = {
        'url': pdf_url,
        'isOverlayRequired': True,
        'apikey': os.getenv('OCR_SPACE_API'),
        'language': 'por',
    }
    response = requests.post('https://api.ocr.space/parse/image', data=payload)
    return response.json()


def parse_contract(response):
    parsed_contract = ''

    try:
        if response.get('ParsedResults'):
            for info in response['ParsedResults']:
                parsed_contract += info['ParsedText']
        parsed_contract = parsed_contract.replace('\r', '').replace('\n', '')
    except AttributeError as e:
        print('Something went wrong: ', e)
    return parsed_contract


def parse_contracts(urls):
    for url in urls:
        if '.pdf' in url:
            response = retrieve_content_from_pdf(url)
            parsed_contract = parse_contract(response)
            # print(parsed_contract)
            filename = url[url.rfind('/')+1:]
            print(filename, find_documents_and_names(parsed_contract))


if __name__ == '__main__':
    urls = open('data/contracts/contracts-url-feira-de-santana-2016-2017.csv').readlines()
    # urls = [
    #     'http://www.transparencia.feiradesantana.ba.gov.br/contratos/06092017134504000000.pdf',
    #     'http://www.transparencia.feiradesantana.ba.gov.br/contratos/06092017134448000000.pdf',
    #     'http://www.transparencia.feiradesantana.ba.gov.br/contratos/06092017134430000000.pdf',
    #     'http://www.transparencia.feiradesantana.ba.gov.br/contratos/06092017134411000000.pdf',
    #     'http://www.transparencia.feiradesantana.ba.gov.br/contratos/06092017134351000000.pdf',
    #     'http://www.transparencia.feiradesantana.ba.gov.br/contratos/06092017134333000000.pdf',
    #     'http://www.transparencia.feiradesantana.ba.gov.br/contratos/06092017134248000000.pdf',
    #     'http://www.transparencia.feiradesantana.ba.gov.br/contratos/06092017134224000000.pdf',
    #     'http://www.transparencia.feiradesantana.ba.gov.br/contratos/06092017134207000000.pdf',
    #     'http://www.transparencia.feiradesantana.ba.gov.br/contratos/06092017134147000000.pdf'

    # ]
    parse_contracts(urls)
