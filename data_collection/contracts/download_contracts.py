from urllib.parse import urljoin
from pathlib import Path

import rows
import scrapy


class FeiraSpider(scrapy.Spider):
    total_pages = 33
    data = {
        "POST_PARAMETRO": "PesquisaContratos",
        "POST_PAGINA": "",
        "POST_PAGINAS": str(total_pages),
        "POST_DATA": "",
        "POST_NMCREDOR": "",
        "POST_CPFCNPJ": "",
        "POST_NUCONTRATO": "",
    }
    download_path = Path(__file__).parent.parent / "data" / "contracts" / "pdfs"
    name = "licitacoes-feira"
    url = "http://www.transparencia.feiradesantana.ba.gov.br/controller/contrato.php"

    def start_requests(self):
        for page in range(1, self.total_pages + 1):
            data = self.data.copy()
            data["POST_PAGINA"] = str(page)
            yield scrapy.FormRequest(url=self.url, formdata=data)

    def parse(self, response):
        # TODO: parse other metadata so we can yield together with PDF URL
        links = rows.plugins.html.extract_links(response.body)
        for link in links:
            if not link.lower().endswith(".pdf"):
                continue

            url = urljoin(self.url, link)
            yield scrapy.Request(url=url, callback=self.save_pdf, meta={"url": url})

    def save_pdf(self, response):
        meta = response.request.meta
        url = meta["url"]
        filename = self.download_path / Path(url).name
        with open(filename, mode="wb") as fobj:
            fobj.write(response.body)
        yield {"download_path": str(filename), "url": url}
