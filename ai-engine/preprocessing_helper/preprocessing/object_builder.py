import uuid
import html
from preprocessing.html_parsers import CustomHtmlParser, HtmlCleaner
from bs4 import BeautifulSoup as bs
from typing import List
from .nlp.contractions import expand_contractions

cleaner = HtmlCleaner()

def pretty_clean(html_str):
    clean_html = cleaner.pretty_clean(html_str)
    soup = bs(clean_html)  
    return soup.prettify()

def remove_duplicate_separators(to_clean: List[str]) -> str:
    clean = to_clean
    result: str = "".join(clean)
    return result
    
def call_pipeline(html_str):
    # Remove only comments, JS, scripts and style tags
    clean_html = " ".join(html.escape(cleaner.bare_html(html_str)).split())
    soup = bs(html_str)
    print(soup.get_text())
    parser = CustomHtmlParser()
    parser.feed(html_str)
    text_list: List[str] = parser.text
    text: str = "".join(text_list)
    text = expand_contractions(text)
    result = {
        "id": str(uuid.uuid4()),
        "text": text,
        "html": clean_html,
        "meta": parser.meta,
        "annotation_approver": None, 
        "labels": []
    }
    print(result)
    return result