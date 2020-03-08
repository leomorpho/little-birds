import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging as log


class CraigslistSpider(scrapy.Spider):
    name = "craigslist"

    def __init__(self, *args, **kwargs):
        super(CraigslistSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs["url"]]
        # open('proxies.txt', 'w').close()

    def parse(self, response):
        # Get craigslist products page policy
        # Find the xpath for product links from policy
        for hdrlnk in response.xpath('//a[contains(@class, "hdrlnk")]/@href').getall():
            full_url = response.urljoin(hdrlnk)
            yield response.follow(hdrlnk, callback=self.parse_hdrlnk, cb_kwargs=dict(url=full_url, policy=""))
        # Find the xpath for next pages from policy
        for href in response.css('.next').xpath('@href'):
            yield response.follow(href, self.parse)

    def parse_hdrlnk(self, response, url, policy):
        # Find each xpath for each field from policy
        yield log.error({
            "title": response.xpath('//*[(@id = "titletextonly")]//text()').get(),
            "price": response.xpath('//*[contains(@class, "price")]//text()').get(),
            "subarea": response.xpath('//nav//li[contains(@class, "subarea")]//a//text()').get(),
            "area": response.xpath('//nav//li[contains(@class, "area")]//a//text()').get(),
            "body": response.css("#postingbody::text").getall(),
            "datetime": response.css(".timeago::text").get().strip(),
            "url": url
        })
