import html
import csv
import typing
import logging 
import os
import config
from html.parser import HTMLParser
from lxml.html.clean import Cleaner
from typing import List
from ..nlp.nlp import preprocessing_pipeline

log = logging.getLogger()
log.setLevel(config.LOG_LEVEL)

# Elements that require text to have a new line ("\n") inserted
NEWLINE_ELEMENTS = {"address", "article", "aside", "blockquote",
                       "details", "dialog", "dd", "div", "dl", "dt",
                       "fieldset", "figcaption", "figure", "footer",
                       "form", "h1", "h2", "h3", "h4", "h5", "h6",
                       "header", "hgroup", "hr", "li", "main", "nav",
                       "ol", "p", "pre", "section", "table", "ul", "br"}

# Inline elements that must be kept in parsed text for semantics
# https://developer.mozilla.org/en-US/docs/Web/HTML/Element
SEMANTIC_ELEMENTS = {"a", "title", "cite", "code", "data", "dfn", "kbd", 
                     "q", "s", "samp", "small", "strong", "sub", "time", "var"}

# MULTIMEDIA_ELEMENTS = {"audio", "img", "map", "track", "video"}
# EMBEDDED_ELEMENTS = {"embed", "iframe", "object", "param", "picture", "source"}
# TABLE_ELEMENTS = {"caption", "col", "colgroup", "table", "tbody", "td", "tfoot", "th", "thead", "tr"}             

class CustomHtmlTarget():
    """A target for an HTML parser based on lxml. Fast."""
    class Results():
        """Class to hold results of parser"""
        def __init__(self):
            # The idea is that short_text will be used to train algorithms,
            # but since it will be heavily cleaned up, it may become hard 
            # to understand for human operator, so I'm also adding a more 
            # understandable version in full_text
            self.short_text: List[str] = []   # For text processing
            self.full_text: List[str] = []    # For human comprehension of short_text
            self.meta: list() = []
            self.meta_words_of_interest: set() = set()
    
    def __init__(self):
        super().__init__()
        self.results = self.Results()
    
    def start(self, tag, attrs) -> None:
        if tag in SEMANTIC_ELEMENTS:
            elem = "<" + tag + ">"
            self.results.full_text.append(elem)
            self.results.short_text.append(elem)
            
        # Extract all useful words from tag attributes
        attrs_list = []
        for attr in attrs:
            attrs_list.append({attr: attrs[attr]})
            important_word_set = preprocessing_pipeline(attrs[attr], html_meta=True)
            if important_word_set:
                self.results.meta_words_of_interest = \
                    self.results.meta_words_of_interest.union(important_word_set)
        if len(attrs_list) > 0:
            self.results.meta = self.results.meta + [{tag: attrs_list}]
        
    def end(self, tag) -> None:
        if tag in SEMANTIC_ELEMENTS:
            elem = "</" + tag + ">"
            self.results.full_text.append(elem)
            self.results.short_text.append(elem)  
        if tag in NEWLINE_ELEMENTS:
            elem = "<br/>"
            self.results.full_text.append(elem)
            self.results.short_text.append(elem)
    
    def data(self, data) -> None:
        for i in data:
            if i.isalnum():
                elem = data
                if elem[0] == " ":
                    elem = elem[1:]
                self.results.full_text.append(elem)
                # short_elem = remove_stopwords(elem)
                # Use string.punctuation to remove ALL punctuation
                # Want to keep: '$'
                # punctuation = '!"#%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
                # elem = elem.translate(str.maketrans('', '', punctuation))
                # elem = expand_contractions(elem)
                # elem = lemmatize_text(elem)
                elem = preprocessing_pipeline(elem, html_meta=False)
                log.error("html_parser:" + str(elem))
                self.results.short_text.extend(elem)
                log.error("short_text in parser:" + str(self.results.short_text))
                break
 
    def comment(self, text) -> None:
        pass
    
    def close(self):
        log.error("short_text in close of parser: " + str(self.results.short_text))
        return self.results



def pretty_clean(html_str: str) -> str:
    cleaner = Cleaner(style=True, 
                        inline_style=True, 
                        links=False, 
                        page_structure=False)
    clean_html = cleaner.clean_html(html_str)
    return clean_html

def bare_html(html_str: str) -> str:
    """Removes all comments, scripts, JS and style tags"""
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
                