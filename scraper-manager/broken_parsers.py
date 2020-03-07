class BrokenWebPageParsers():
    def __init__(self):
        # Connect to db and extract all broken webpage parsers
        # Load every item into a BrokenWebPageParser object
        self.broken_webpage_parsers = []
        pass

    def get_broken_webpage_parsers(self):
        return self.broken_webpage_parsers

    def get_broken_pages_number(self):
        return len(self.broken_webpage_parsers)


class BrokenWebPageParser():
    def __init__(self, url):
        self.url = url
    
    def get_page_model(self):
        pass

    def get_broken_fields(self):
        pass

    def get_broken_fields_length(self):
        pass
