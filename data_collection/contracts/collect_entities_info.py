from functools import lru_cache
import pandas as pd
import os
import requests
import requests_cache
import time
from data_collection.contracts.utils import make_document_valid


ONE_DAY_IN_SECONDS = 86400


class BrasilIOAPI:
    """
    Source: https://brasil.io/dataset/documentos-brasil/documents
    """
    API_URL = 'https://brasil.io/api/dataset/documentos-brasil/documents/data'
    CACHE_NAME = 'contracts/brasilio_cache'

    def get_document_info(self, document_id):
        response = requests.get(
            self.API_URL,
            params={'document': document_id}
        ).json()
        if response['count'] == 0:
            return {document_id: {}}
        return  {document_id: response['results'][response['count'] - 1]}


class ReceitaWs:
    """
    Source: https://receitaws.com.br/
    """
    TOKEN = os.getenv('RECEITAWS_API_TOKEN')
    API_URL = 'https://www.receitaws.com.br/v1/cnpj'
    CACHE_NAME = 'contracts/brasilws_cache'
    
    def _request(self, document_id):
        if not document_id:
            return
        response = requests.get(
            f'{self.API_URL}/{document_id}',
            headers={'Authorization': f'Bearer {self.TOKEN}'}
        ).json()
        time.sleep(20)
        return {document_id: response}
    
    def get_document_info(self, document_id):
        try:
            return self._request(document_id)
        except:
            time.sleep(30)

contracts = pd.read_excel('data/contratos-prefeitura-2016-2017.xls')
documents = contracts['CPF/CNPJ'].unique()
# print(f'Unique {len(documents)} documents.')

search_method = BrasilIOAPI()
requests_cache.install_cache(cache_name=search_method.CACHE_NAME, backend='sqlite', expire_after=ONE_DAY_IN_SECONDS)


for document_id in documents:
    document = str(document_id)
    valid_document = make_document_valid(document)
    print(search_method.get_document_info(valid_document))
