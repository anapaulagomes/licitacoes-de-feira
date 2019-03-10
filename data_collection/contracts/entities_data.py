import os
import requests
import requests_cache


ONE_WEEK_IN_SECONDS = 86400 * 7


class BrasilIOAPI:
    """
    Source: https://brasil.io/dataset/documentos-brasil/documents
    """

    API_URL = "https://brasil.io/api/dataset/documentos-brasil/documents/data"
    CACHE_NAME = "contracts/brasilio_cache"

    def __init__(self):
        self.cache = requests_cache.install_cache(
            cache_name=self.CACHE_NAME,
            backend="sqlite",
            expire_after=ONE_WEEK_IN_SECONDS,
        )

    def get_document_info(self, document_id):
        response = requests.get(self.API_URL, params={"document": document_id}).json()
        if response["count"] == 0:
            return {}
        return response["results"][response["count"] - 1]


class ReceitaWs:
    """
    Source: https://receitaws.com.br/
    """

    TOKEN = os.getenv("RECEITAWS_API_TOKEN")
    API_URL = "https://www.receitaws.com.br/v1/cnpj"
    CACHE_NAME = "contracts/brasilws_cache"

    def __init__(self):
        self.cache = requests_cache.install_cache(
            cache_name=self.CACHE_NAME,
            backend="sqlite",
            expire_after=ONE_WEEK_IN_SECONDS,
        )

    def _request(self, document_id):
        if not document_id:
            return
        response = requests.get(
            f"{self.API_URL}/{document_id}",
            headers={"Authorization": f"Bearer {self.TOKEN}"},
        )
        print(response, response.json())
        return response

    def get_document_info(self, document_id):
        try:
            response = self._request(document_id)
            if response.status_code == 504:
                time.sleep(25)
                response = self._request(document_id)
            return response.json()

        except Exception as e:
            print(f"Request failed (doc_id={document_id}). Slepping for 35 seconds...")
            print(str(e))
            time.sleep(35)


brasilio = BrasilIOAPI()
receitaws = ReceitaWs()
