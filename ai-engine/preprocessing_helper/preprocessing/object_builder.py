import uuid
from preprocessing.html_parsers import CustomHtmlParser, HtmlCleaner
from bs4 import BeautifulSoup as bs

cleaner = HtmlCleaner()

def pretty_clean(html_str):
        clean_html = cleaner.pretty_clean(html_str)
        soup = bs(clean_html)  
        return soup.prettify()
    
def pipeline_result(html_str):
    parser = CustomHtmlParser()
    parser.feed(html_str)
    result = {
        "id": str(uuid.uuid4()),
        "text": parser.text,
        "html": html_str,
        "meta": parser.meta,
        "annotation_approver": None, 
        "labels": []
    }
    return result