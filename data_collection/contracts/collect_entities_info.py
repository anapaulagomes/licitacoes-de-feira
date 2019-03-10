import json
import os
import requests
import requests_cache
import rows
import time
from utils import make_document_valid


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
        ).json()
        time.sleep(20)
        return response

    def get_document_info(self, document_id):
        try:
            return self._request(document_id)
        except:
            time.sleep(30)


def consolidate_entities(raw_docs_from_contract):
    docs_from_contract = {}
    for doc in raw_docs_from_contract:
        if docs_from_contract.get(doc.name):
            if doc.document not in docs_from_contract[doc.name]["documents"]:
                docs_from_contract[doc.name]["documents"].append(
                    str(doc.document).strip(".0")
                )
            legal_representant = {
                "name": doc.legal_representant,
                "document": str(doc.legal_representant_document).strip(".0"),
            }
            if (
                legal_representant
                not in docs_from_contract[doc.name]["legal_representants"]
            ):
                docs_from_contract[doc.name]["legal_representants"].append(
                    legal_representant
                )
        else:
            docs_from_contract[doc.name] = {
                "documents": [str(doc.document).strip(".0")],
                "legal_representants": [
                    {
                        "name": doc.legal_representant,
                        "document": str(doc.legal_representant_document).strip(".0"),
                    }
                ],
            }
    return docs_from_contract


contracts = rows.import_from_xls("data/contracts/city-hall-contracts-2016-2017.xls")
raw_docs_from_contract = rows.import_from_csv(
    "data/contracts/documents-from-contracts.csv"
)

documents = set(contracts["cpfcnpj"])
docs_from_contract = consolidate_entities(raw_docs_from_contract)

brasilio = BrasilIOAPI()

invalid_document = []
entities = {}
for contract in contracts:
    contract_info = {
        "code": contract.no_contrato,
        "description": contract.objeto,
        "start_date": contract.inicio_do_contrato,
        "end_date": contract.fim_do_contrato,
        "cost": contract.valorr,
    }

    # fix invalid document if invalid
    valid_document = make_document_valid(str(contract.cpfcnpj))
    if str(contract.cpfcnpj) != valid_document:
        invalid_document.append(str(contract.cpfcnpj))

    if entities.get(valid_document):
        entities[valid_document]["contracts"].append(contract_info)
    else:
        name = contract.contratada.lstrip().rstrip()
        entity = {
            "name": name,  # taking into account that at least the name is right
            "document": valid_document,
            "document_type": "CNPJ" if len(valid_document) == 14 else "CPF",
            "sources": ["website-contracts"],
            "contracts": [contract_info],
        }

        # get info from parsed PDFs
        doc_from_contract = docs_from_contract.get(contract.contratada)
        if doc_from_contract:
            entity["sources"].append("parsed-contracts")
            entity["legal_representants"] = doc_from_contract["legal_representants"]

        # get info on brasil io
        result = brasilio.get_document_info(valid_document)
        if not result and doc_from_contract:
            for doc in doc_from_contract["documents"]:
                if doc != valid_document:
                    result = brasilio.get_document_info(valid_document)
                    if result:
                        break
        if result:
            entity["sources"].append("brasil-io")
            entity["name"] = result["name"]
            entity["document"] = result["document"]
            entity["document_type"] = result["document_type"]

        entities[valid_document] = entity


with open("data/contracts/entities.json", "w") as outfile:
    json.dump(entities, outfile)

print(f"Unique {len(documents)} documents - Invalid: {len(set(invalid_document))}")
print(f"Found entities: {len(entities)} Number of contracts: {len(contracts)}")
