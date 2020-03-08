import argparse
from main.search_engine import SearchEngine, process
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


process = CrawlerProcess(get_project_settings())

parser = argparse.ArgumentParser(description='A craigslist spider')
parser.add_argument("-k", "--keywords", default=1, type=str,
                    help="A string of keyword(s) such as 'air compressor'. \
                It can be multiple words but must represent a single object", required=True)
parser.add_argument("-l", "--location", default=1,
                    type=str, help="A string of a location such as 'Maple Ridge, BC'", required=True)

args = parser.parse_args()

if args.keywords and args.location:
    print(f"Searching for '{args.keywords}' in '{args.location}'")


def main():
    keywords = args.keywords
    location = args.location

    open('proxies.txt', 'w').close()
    process.crawl('freeproxy')

    searchEngine = SearchEngine()

    query = {
        'keywords': args.keywords,
        'location': args.location
    }
    sites = (['craigslist'])

    searchEngine.search(query=query, sites=sites)

    # Start all spiders
    process.start(stop_after_crawl=True)


if __name__ == "__main__":
    main()
