import uuid
import html
from lxml.html.clean import Cleaner
from bs4 import BeautifulSoup as bs

class CustomHtmlParser(html.parser.HTMLParser):
    meta = list()
    text = ""
    def handle_data(self, data):
        print(data)
        data = data.strip()
        for i in data:
            if i.isalnum():
                self.text += data + "\n"
            break
  
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            self.meta.append([tag, attr])
            

class HtmlCleaner():
    def pretty_clean(self, html_str):
        cleaner = Cleaner(style=True, 
                          inline_style=True, 
                          links=False, 
                          page_structure=False)
        clean_html = cleaner.clean_html(html_str)
        return clean_html
    
    def pipeline_result(self, html_str):
        tags_to_remove = ["b", "strong", "i", "em", "mark", "small", "del", "ins", "sub", "sup"]
        cleaner = Cleaner(style=True, 
                          inline_style=True,
                          scripts=True,
                          javascript=True,
                          comments=True,
                          links=False, 
                          remove_tags=tags_to_remove,
                          forms=False)
        html_clean = cleaner.clean_html(html_str)
        return html_clean