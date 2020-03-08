from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging as log


class PolicySpider(Spider):
    name = "policy"

    def __init__(self, *args, **kwargs):
        super(PolicySpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs["url"]]
        # open('proxies.txt', 'w').close()

    def parse(self, response):
        # Get scraping policy for this page
        
        # If this policy has fields to be scraped and populated, do it now

        # If this policy has links to be crawled, crawl them 
        
        
