from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.http import FormRequest
import logging


class KijijiSpider(Spider):
    name = "kijiji"

    start_urls = ['https://www.kijiji.ca/']

    def parse(self, response):
        return FormRequest.from_response(
                response,
                formdata={
                    'keywords': 'air compressor',
                    'address': 'Maple Ridge',
                    'minPrice': '',
                    'maxPrice': '',},
                callback=self.parse_search_results
                )

    def parse_search_results(self, response):
        for hdrlnk in response.xpath('//div[@class="info"]//@href').getall():
            full_url = response.urljoin(hdrlnk)
            yield response.follow(hdrlnk, callback=self.parse_hdrlnk, cb_kwargs=dict(url=full_url))
        for href in response.xpath('//div[@class="pagination"]//*[@title="Next"]//@href'):
            yield response.follow(href, self.parse)

    def parse_hdrlnk(self, response, url):
        yield {
            "title": response.xpath('//h1[contains(@class, "title")]//text()').get(),
            "price": response.xpath('//h1[contains(@class, "title")]/following-sibling::*//text()').getall(),
            "location": response.xpath('//*[contains(@*, "address")]//text()').get(),
            "description": response.xpath('//h3[text()="Description"]/following-sibling::div').getall(),
            "datetime": response.xpath('//time/@datetime').get(),
            "url": url
        }
