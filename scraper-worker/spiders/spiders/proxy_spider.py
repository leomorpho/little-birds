from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging as log
from lxml import etree
from io import StringIO
import re


class FreeProxySpider(Spider):
    name = "freeproxy"

    def __init__(self, *a, **kw):
        super(FreeProxySpider, self).__init__(*a, **kw)
        open('proxies.txt', 'w').close()

    start_urls = [
        'https://free-proxy-list.net/',
        'https://www.us-proxy.org/',
        'https://free-proxy-list.net/uk-proxy.html',
        'https://www.sslproxies.org/',
        'https://free-proxy-list.net/anonymous-proxy.html',
        'http://www.google-proxy.net/'
    ]

    def parse(self, response):
        proxies = set()
        for proxy in response.xpath('//table/tbody/tr').getall():
            proxy_types = ['elite', 'anonymous']
            if any(x in proxy.lower() for x in proxy_types):
                proxies.add(proxy)
        proxies = self.parse_proxies(proxies)
        self.save_proxies(proxies)
        log.info(f"{len(proxies)} new proxies saved")

        for href in response.xpath('//a[contains(text(), "Next")]/@href'):
            yield response.follow(href, self.parse)

    def parse_proxies(self, proxies):
        parsed_proxies = []
        for x in proxies:
            parser = etree.HTMLParser()
            tree = etree.parse(StringIO(x), parser)
            proxy_ip = ''
            proxy_port = ''
            try:
                proxy_ip = str(tree.xpath('//tr/td[1]//text()')[0])
                proxy_port = str(tree.xpath('//tr/td[2]//text()')[0])
            except IndexError:
                pass
            except Exception as exc:
                log.error(exc)

            if re.search(r'(\d+)\.(\d+)\.(\d+)\.(\d+)', proxy_ip) and re.search(r'(\d+)', proxy_port):
                new_proxy = proxy_ip + ":" + proxy_port
                # log.debug(f"New proxy: {new_proxy}")
                parsed_proxies.append(new_proxy)
        return parsed_proxies

    def save_proxies(self, proxies):
        """@proxies: set of proxies"""
        for x in proxies:
            with open('proxies.txt', 'a+') as f:
                f.write(x + '\n')


# May need to add logic to clean up blocked proxies
