import uuid
import html
from preprocessing.html_parsers import HtmlCleaner, CustomHtmlTarget, MetaWordsImprover
from bs4 import BeautifulSoup as bs
from typing import List
from lxml import etree
from .nlp.constants_en import META_WORDS_OF_INTEREST

cleaner = HtmlCleaner()

def pretty_clean(html_str: str) -> str:
    clean_html = cleaner.pretty_clean(html_str)
    soup = bs(clean_html, "html.parser")  
    return soup.prettify()

def pprint_unescape(escaped_html_str: str) -> str:
    unescaped = html.unescape(escaped_html_str)
    soup = bs(unescaped, "html.parser")
    return soup.prettify()
    
def call_pipeline(html_str: str) -> str:
    parser = etree.HTMLParser(
        target=CustomHtmlTarget(), 
        remove_blank_text=True,
        remove_comments=True,
        remove_pis=True)
    result = etree.HTML(html_str, parser)
    
    # The following is not efficient, but lxml parser keeps adding root tags 
    # (html, body) to "incomplete" html strings. Since I only want to preserve
    #  the original, this is not ok, and I use a different parser to get the 
    # clean raw html. Since I only save the raw html for my corpus, the expense
    # is not that significant...
    raw_html = cleaner.bare_html(html_str)
    raw_html = html.escape(" ".join(raw_html.split()))
    
    uuid_str = str(uuid.uuid4())
    short_text = result.short_text.strip()
    full_text = result.full_text.strip()
    
    # Persist words of interest to DB to sort them by prevalence and select new good ones
    # to add to META_WORDS_OF_INTEREST and USELESS_HTML_ATTRS_CONSTANTS
    meta_words_of_interest = result.meta_words_of_interest
    meta_words_improver = MetaWordsImprover()
    meta_words_improver.update_list(meta_words_of_interest)
    # meta_words_improver.update_list(meta_words_of_interest)
    
    meta_words_of_interest = list(meta_words_of_interest & META_WORDS_OF_INTEREST)
    meta = result.meta
    
    obj = {
        "id": uuid_str,
        "text": short_text,
        "full_text": full_text,
        "meta_words_of_interest": meta_words_of_interest,
        "meta": meta,
        "annotation_approver": None, 
        "labels": [],
        "html": raw_html
    }
    return obj

def pipeline_on_saved_data() -> None:
    # Add button in UI to save html (with url) to DB. Should there also be an option 
    # to add words to the metawords (like handpicked categories). This option would 
    # need autocomplete to be sure not to create too many
    pass