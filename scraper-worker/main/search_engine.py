from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import logging as log

process = CrawlerProcess(get_project_settings())


class SearchEngine():
    def __init__(self):
        self._search_engine_factory = _SearchEngineFactory()
        self._search_engine_factory.register_search_engine(
            'craigslist', _CraigslistSearchEngine)

    def search(self, query, sites):
        """Search a query on a list of sites
        @param query (dict) dictionnary of query fields
        @param sites (list) list of sites to search
        """
        for site in sites:
            search_engine = self._search_engine_factory.get_search_engine(site)
            search_engine().search(query)


class _SearchEngineFactory():
    def __init__(self):
        self._search_engines = {}

    def register_search_engine(self, site, search_engine):
        """Register a site to a specific search engine class"""
        self._search_engines[site] = search_engine

    def get_search_engine(self, site):
        """Return search engine corresponding to given site"""
        search_engine = self._search_engines.get(site)
        if not search_engine:
            raise ValueError(site)
        return search_engine


class _CraigslistSearchEngine():
    def __init__(self):
        self.domain = 'craigslist'

    def search(self, query):
        """Search given query
        @param (dict) dictionnary of query fields
        """
        url = self._build_url(query)
        # Set start_url of craigslist spider
        process.crawl('craigslist', url=url)
        process.start(stop_after_crawl=True)

    def _build_url(self, query):
        # location = parse_location(keywords['location'], site=self.domain)
        keywords = '+'.join(query['keywords'].split())
        url = 'https://vancouver.craigslist.org/search/sss?query=' + keywords + '&sort=rel'
        log.error(url)
        return url
