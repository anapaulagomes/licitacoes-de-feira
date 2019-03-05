import scrapy
import re


class AllBidsSpider(scrapy.Spider):
    name = "all_bids"
    start_urls = ["http://www.feiradesantana.ba.gov.br/seadm/licitacoes.asp"]
    bid_id = 0

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
        raw_descriptions = response.xpath(
            "//table/tr[2]/td/table/tr[6]/td/table/tr/td[2]/table[1]"
        )
        raw_bids_history = response.xpath(
            "//table/tr[2]/td/table/tr[6]/td/table/tr/td[2]/table[2]"
        )
        raw_when = response.xpath("//tr/td[3]/table/tr/td/text()").extract()
        descriptions = self._parse_descriptions(raw_descriptions)
        bids_history = self._parse_bids_history(raw_bids_history)
        modalities = self._parse_modalities(raw_modalities)
        when = self._parse_when(raw_when)

        for modality, (description, document_url), bid_history, when in zip(
            modalities, descriptions, bids_history, when
        ):
            url_pattern = re.compile(r"licitacoes_pm\.asp\?cat=(\w+)\&dt=(\d+-\d+)")
            match = url_pattern.search(response._url)

            yield {
                "id": self.bid_id,
                "url": response._url,
                "category": match.group(1),
                "month_year": match.group(2),
                "description": description,
                "history": bid_history,
                "modality": modality,
                "when": when,
                "document_url": document_url,
            }

            self.bid_id += 1

    def _parse_descriptions(self, raw_descriptions):
        descriptions = []
        for raw_description in raw_descriptions:
            description = raw_description.xpath(".//text()").extract()
            document_url = raw_description.xpath(".//@href").extract_first()
            description = self._parse_description(description)

            if description != "Objeto":
                document_url = document_url if document_url else ""
                descriptions.append((description, document_url))
        return descriptions
    
    def _parse_bids_history(self, raw_bids_history):
        all_bids_history = []
        for raw_bid_history in raw_bids_history:
            bids_history = []
            for row in raw_bid_history.xpath(".//tr"):
                when = row.xpath(".//td[2]/text()").get().strip()
                event = row.xpath(".//td[3]/div/text()").get()
                url = row.xpath(".//td[4]/div/a//@href").get()

                if event and when:
                    bids_history.append(
                        {"when": when, "event": event.capitalize(), "url": url if url else ""}
                    )
            all_bids_history.append(bids_history)

        return all_bids_history

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
                modality = modality.replace("\r\n", " / ")
                modalities.append(modality)
        return modalities

    def _parse_when(self, raw_when):
        return [date[1:] for date in raw_when]
