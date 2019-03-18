import json
import rows
import time
from data_colltion.utils import make_document_valid


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


raw_contracts = rows.import_from_xls("data/contracts/city-hall-contracts-2016-2017.xls")
raw_docs_from_contract = rows.import_from_csv(
    "data/contracts/documents-from-contracts.csv"
)

documents = set(raw_contracts["cpfcnpj"])
docs_from_contract = consolidate_entities(raw_docs_from_contract)


invalid_document = []
contracts = []
for contract in raw_contracts:
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

    name = contract.contratada.lstrip().rstrip()
    entity = {
        "name": name,  # taking into account that at least the name is right
        "document": valid_document,
        "document_type": "CNPJ" if len(valid_document) == 14 else "CPF",
        "sources": ["website-contracts"],
        "data_from_pdf": {},
    }

    # get info from parsed PDFs
    doc_from_contract = docs_from_contract.get(contract.contratada)
    if doc_from_contract:
        entity["sources"].append("parsed-contracts")
        entity["data_from_pdf"] = doc_from_contract

    contract_info["contractor"] = entity
    contracts.append(contract_info)


with open("data/contracts/contracts.json", "w") as outfile:
    json.dump(contracts, outfile)

print(f"Unique {len(documents)} documents - Invalid: {len(set(invalid_document))}")
print(
    f"Consolidate contracts: {len(contracts)} Number of contracts from XLS: {len(contracts)}"
)
