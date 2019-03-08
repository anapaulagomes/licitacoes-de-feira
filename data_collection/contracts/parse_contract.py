import os
import pandas as pd
import re
import requests
import requests_cache
from io import StringIO


ONE_DAY_IN_SECONDS = 86400
CNPJ_PATTERN = re.compile(r'\d{2}\.\d{3}\.\d{3}[\/|.]\d{4}-\d{2}')
CPF_PATTERN = re.compile(r'\d{3}\.\d{3}\.\d{3}-\d{2}')
CNPJ_OR_CPF_PATTERN = re.compile(r'\d{2}\.\d{3}\.\d{3}[\/|.]\d{4}-\d{2}|\d{3}\.\d{3}\.\d{3}-\d{2}')
CONTRACT_HEADER_PATTERN = re.compile(r'do outro lado,(.*) |cláusulas e condições seguintes')
LEGAL_REPRESENTANT_PATTERN = re.compile(r'representante legal,?(.+?),')

requests_cache.install_cache(cache_name='contracts/ocrspace_cache', backend='sqlite', expire_after=ONE_DAY_IN_SECONDS)


def clean_string(string):
    string = re.sub(r'[^\w]', ' ', string)
    return string.lstrip().rstrip()


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
        cleaned_document = clean_string(documents[0])
        return cleaned_document.replace(' ', '')
    return None


def find_documents_and_names(sample):
    header = re.findall(CONTRACT_HEADER_PATTERN, sample)
    if header:
        header = header[0]
        name = parse_name(header)
        index_name = header.find(name)
        header = header[index_name:]
        
        legal_representant = parse_legal_representant(header)

        document_header = re.findall(f'{name}(.*){legal_representant}', header)
        document = None
        if document_header:
            document_header = document_header[0]
            document = parse_documents(document_header)
            header = header.replace(document_header, '')

        legal_representant_document = parse_documents(header)

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


if __name__ == '__main__':
    urls = pd.read_csv('data/contracts-url-feira-de-santana-2016-2017.csv')

    for _, document in urls.iterrows():
        response = retrieve_content_from_pdf(document['url'])
        parsed_contract = parse_contract(response)
        # print(parse_contract)
        print(find_documents_and_names(parsed_contract))
