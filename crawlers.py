import scrapy
import re


class BidSpider(scrapy.Spider):
    name = "bid"
    start_urls = ["http://www.feiradesantana.ba.gov.br/seadm/licitacoes.asp"]

    def parse(self, response):
        all_bidding_urls = response.xpath("//table/tbody/tr/td/div/a//@href").extract()
        base_url = "http://www.feiradesantana.ba.gov.br/seadm/"

        url_pattern = re.compile(r"licitacoes_pm\.asp\?cat=\w+\&dt=\d+-\d+")

        for url in all_bidding_urls:
            match = url_pattern.search(url)
            if match:
                yield response.follow(f"{base_url}{match.group()}", self.parse_page)

    def parse_page(self, response):
        raw_modalities = response.xpath("//tr/td[1]/table/tr/td/text()").extract()
        raw_descriptions = response.selector.select(
            "//table/tr[2]/td/table/tr[6]/td/table/tr/td[2]"
        )
        raw_when = response.xpath("//tr/td[3]/table/tr/td/text()").extract()
        descriptions = self._parse_descriptions(raw_descriptions)
        modalities = self._parse_modalities(raw_modalities)
        when = self._parse_when(raw_when)

        for modality, (description, document_url), when in zip(
            modalities, descriptions, when
        ):
            url_pattern = re.compile(r"licitacoes_pm\.asp\?cat=(\w+)\&dt=(\d+-\d+)")
            match = url_pattern.search(response._url)

            yield {
                "url": response._url,
                "category": match.group(1),
                "month_year": match.group(2),
                "description": description,
                "modality": modality,
                "when": when,
                "document_url": document_url,
            }

    def _parse_descriptions(self, raw_descriptions):
        descriptions = []
        for raw_description in raw_descriptions:
            description = raw_description.select(".//text()").extract()
            document_url = raw_description.xpath(".//@href").extract_first()
            description = self._parse_description(description)
            if description != "Objeto":
                document_url = document_url if document_url else ""
                descriptions.append((description, document_url))
        return descriptions

    def _parse_description(self, raw_descriptions):
        descriptions = []
        for raw_description in raw_descriptions:
            description = raw_description.strip()
            if not description.isspace():
                descriptions.append(description)
        return "".join(descriptions)

    def _parse_modalities(self, raw_modalities):
        modalities = []
        for raw_modality in raw_modalities:
            modality = raw_modality.strip()
            if modality != "":
                modalities.append(modality)
        return modalities

    def _parse_when(self, raw_when):
        return [date[1:] for date in raw_when]
