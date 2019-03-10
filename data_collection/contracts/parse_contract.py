import csv
import os
import re
import rows

ONE_DAY_IN_SECONDS = 86400
CNPJ_PATTERN = re.compile(r"\d{2}\.\d{3}\.\d{3}[\/|.]\d{4}-\d{2}")
CPF_PATTERN = re.compile(r"\d{3}\.\d{3}\.\d{3}-\d{2}")
CNPJ_OR_CPF_PATTERN = re.compile(
    r"\d{2}\S+\d{3}\S+\d{3}\S+\d{4}.*?\d{2}|\d{3}\S+\d{3}\S+\d{3}.*?\d{2}"
)
CONTRACT_HEADER_PATTERN = re.compile(
    r"do outro lado,(.*) (condições seguintes|CLÁUSULA PRIMEIRA)"
)
LEGAL_REPRESENTANT_PATTERN = re.compile(
    r"(representante.+?|representada por.+?) (.+?),"
)


def clean_document(string):
    string = re.sub(r"[^\w]", " ", string)
    string = string.replace(" ", "")
    string = string.lstrip().rstrip()
    if len(string) == 15 and "10001" in string:
        # a few cnpjs are replacing / by 1 during PDF parser process
        return string.replace("10001", "0001")
    return string


def clean_string(string):
    words = string.split(" ")
    # removing symbols in the middle of the name
    for word in words:
        string = re.sub(r"[^\w]", " ", string)
    return " ".join([re.sub(r"[^\w]", " ", word).replace(" ", "") for word in words])


def parse_name(header):
    index_name = header.find(",")
    name = header[:index_name]
    return name.lstrip().rstrip()


def parse_legal_representant(header):
    salutations = ["Sr ", "Sra ", "Sr,(a) ", "Sr. ", "Sr.(a) ", "Sria "]
    for salutation in salutations:
        if salutation in header:
            header = header.replace(salutation, "")
    legal_representant = re.findall(LEGAL_REPRESENTANT_PATTERN, header)
    if legal_representant != []:
        return clean_string(legal_representant[0][1])
    return None


def parse_documents(header):
    documents = re.findall(CNPJ_OR_CPF_PATTERN, header)
    if documents:
        return [clean_document(document) for document in documents]
    return []


def find_documents_and_names(sample):
    header = re.findall(CONTRACT_HEADER_PATTERN, sample)
    if header:
        header = header[0][0]
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
            "name": name,
            "document": document,
            "legal_representant": legal_representant,
            "legal_representant_document": legal_representant_document,
        }
    return {}


def extract_content(file_content):
    pages = rows.plugins.pdf.pdf_to_text(file_content)
    parsed_contract = "".join(pages).replace("\r", "").replace("\n", "")
    result = {"error": None, "result": {}}
    if parsed_contract != "":
        result["result"] = find_documents_and_names(parsed_contract)
    else:
        result["error"] = "This PDF is probably an image"
    return result


if __name__ == "__main__":
    pds_directory = "data/contracts/pdfs/"

    not_found = 0
    image = 0
    error = 0
    key_not_found = {
        "name": 0,
        "document": 0,
        "legal_representant": 0,
        "legal_representant_document": 0,
    }
    invalid_document = {"document": 0, "legal_representant_document": 0}

    pdfs = os.listdir(pds_directory)
    results = []
    for pdf in pdfs:
        if ".pdf" in pdf:
            result = extract_content(open(pds_directory + pdf))

            if result["result"] == {}:
                if result["error"] == "This PDF is probably an image":
                    image += 1
                else:
                    not_found += 1
                    print(pds_directory + pdf)
                continue
            elif result["error"] is None:
                output = result["result"]
                output["pdf"] = pdf
                results.append(output)

            for key, value in result["result"].items():
                if value == "" or value is None:
                    key_not_found[key] = key_not_found[key] + 1
                elif key == "document" or key == "legal_representant_document":
                    if len(value) != 11 and len(value) != 14:
                        invalid_document[key] = invalid_document[key] + 1

    with open(
        "data/contracts/documents-from-contracts.csv", "w", encoding="utf8", newline=""
    ) as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=results[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(results)

    total = len(pdfs)
    print("------------------------------------------")
    print(
        f"Total: {total} [Image: {image} ({image*100//total}%) Not found: {not_found} ({not_found*100//total}%) Error: {error} ({error*100//total}%)]"
    )
    print("------------------------------------------")
    print(f"Key not found: {key_not_found}")
    print(f"Invalid document: {invalid_document}")
