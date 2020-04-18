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
                       "ol", "p", "pre", "section", "table", "ul"}

# Inline elements that must be kept in parsed text for semantics
# https://developer.mozilla.org/en-US/docs/Web/HTML/Element
SEMANTIC_ELEMENTS = {"a", "title", "cite", "code", "data", "dfn", "kbd", 
                     "q", "s", "samp", "small", "strong", "sub", "time", "var"}

# MULTIMEDIA_ELEMENTS = {"audio", "img", "map", "track", "video"}
# EMBEDDED_ELEMENTS = {"embed", "iframe", "object", "param", "picture", "source"}
# TABLE_ELEMENTS = {"caption", "col", "colgroup", "table", "tbody", "td", "tfoot", "th", "thead", "tr"}             

HTML_NEWLINE_ELEM = "<br/>"

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
        if tag in [HTML_NEWLINE_ELEM, "br"]:
            self.results.full_text.append(HTML_NEWLINE_ELEM)
            self.results.short_text.append(HTML_NEWLINE_ELEM)
        elif tag in SEMANTIC_ELEMENTS:
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
            self.results.full_text.append(HTML_NEWLINE_ELEM)
            self.results.short_text.append(HTML_NEWLINE_ELEM)
    
    def data(self, data) -> None:
        remove_extra_newline_elem(self.results.short_text, self.results.full_text)
            
        # #log.info(self.results.full_text)
        # if len(self.results.full_text) == 0:
        #     pass
        # elif is_not_blank(data) and self.results.full_text[-1] == HTML_NEWLINE_ELEM:
        #     # If there's no data and last added element is a html newline,
        #     # then we want to remove that last elem. It's a bit cumbersome,
        #     # but the parser can't look into the future to see if the node has
        #     # data, so intead we do the work, and undo it if there's no data.
        #     # log.error(self.results.full_text[-1])
        #     self.results.full_text.pop()
        #     self.results.short_text.pop()
        
        if is_not_blank(data):
            # if elem[0] == " ":
            #     elem = elem[1:]
            self.results.full_text.append(data.strip())
            # short_elem = remove_stopwords(elem)
            # Use string.punctuation to remove ALL punctuation
            # Want to keep: '$'
            # punctuation = '!"#%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
            # elem = elem.translate(str.maketrans('', '', punctuation))
            # elem = expand_contractions(elem)
            # elem = lemmatize_text(elem)
            data = preprocessing_pipeline(data, html_meta=False, remove_stopwords=True)
            self.results.short_text.extend(data)
 
    def comment(self, text) -> None:
        pass
    
    def close(self):
        remove_extra_newline_elem(self.results.short_text, self.results.full_text)
        return self.results
    
def remove_extra_newline_elem(short_text, full_text: List[str]):
    if len(full_text) > 2 and full_text[-1] == HTML_NEWLINE_ELEM \
                        and full_text[-2] == HTML_NEWLINE_ELEM:
        full_text.pop()
        short_text.pop()


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

# TODO: For now, I don't care if there are empty html elements...
# def remove_empty_html_elems_caller(word_list: List[str]) -> List[str]:
#     # This probably needs to be recursive
#     return word_list

# def remove_empty_html_elems(x: List[str]) -> bool:
#     # # Don't touch <br/> elements
#     # if x[0] == HTML_NEWLINE_ELEM:
#     #     pass
#     # If first elem is an opening tag
#     if x[0][0] == "<" and x[0][-1] != "/":
#         # If has content, return list
        
#         # If has no content, call f on [1:]
#         pass
#     # If first elem is a closing tag
#     elif x[0][0] == "<" and x[0][-1] == "/":
#         if x[0] == HTML_NEWLINE_ELEM:
#             return x
            
#         pass

def is_not_blank(s):
    return bool(s and s.strip())