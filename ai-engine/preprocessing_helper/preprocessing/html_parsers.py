import html
import csv
import typing
import logging 
import os
from html.parser import HTMLParser
from lxml.html.clean import Cleaner
from .nlp.utils import remove_stopwords, lemmatize_text, important_words, expand_contractions

log = logging.getLogger()
log.setLevel(logging.DEBUG)

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
    class Result():
        """Class to hold results of parser"""
        def __init__(self):
            # The idea is that short_text will be used to train algorithms,
            # but since it will be heavily cleaned up, it may become hard 
            # to understand for human operator, so I'm also adding a more 
            # understandable version in full_text
            self.short_text: str = ""   # For text processing
            self.full_text: str = ""   # For human comprehension of short_text
            self.meta: list() = []
            self.meta_words_of_interest: set() = set()
    
    results = Result()
    
    def start(self, tag, attrs) -> None:
        if tag in SEMANTIC_ELEMENTS:
            elem = "<" + tag + ">"
            self.results.full_text += elem
            self.results.short_text += elem
            
        # Extract all useful words from tag attributes
        attrs_list = []
        for attr in attrs:
            attrs_list.append({attr: attrs[attr]})
            important_word_set = important_words(attrs[attr])
            if important_word_set:
                self.results.meta_words_of_interest = \
                    self.results.meta_words_of_interest.union(important_word_set)
        self.results.meta.append(str((tag, attrs_list)))
        
    def end(self, tag) -> None:
        if tag in SEMANTIC_ELEMENTS:
            elem = "<" + tag + "/>"
            self.results.full_text += elem
            self.results.short_text += elem   
        if tag in NEWLINE_ELEMENTS:
            elem = " "
            self.results.full_text += elem
            self.results.short_text += elem
    
    def data(self, data) -> None:
        for i in data:
            if i.isalnum():
                elem = data
                if elem[0] == " ":
                    elem = elem[1:]
                short_elem = expand_contractions(elem)
                self.results.full_text += elem + " "
                # Use string.punctuation to remove ALL punctuation
                # Want to keep: '$'
                # punctuation = '!"#%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
                # short_elem = short_elem.translate(str.maketrans('', '', punctuation))
                short_elem = remove_stopwords(short_elem)
                short_elem = lemmatize_text(short_elem)
                self.results.short_text += short_elem + " "
                break
 
    def comment(self, text) -> None:
        pass
    
    def close(self):
        return self.results


class HtmlCleaner():
    def pretty_clean(self, html_str: str) -> str:
        cleaner = Cleaner(style=True, 
                          inline_style=True, 
                          links=False, 
                          page_structure=False)
        clean_html = cleaner.clean_html(html_str)
        return clean_html
    
    def bare_html(self, html_str: str) -> str:
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
  
    
class MetaWordsImprover():
    def __init__(self):
        self.dir_name = "metawords_data"
        self.filename_metawords = self.dir_name + "/metawords.csv"
        
        if os.path.isdir(self.dir_name) is False:
            os.mkdir(self.dir_name)
        if os.path.exists(self.filename_metawords) is False:
            log.error("creating csv file")
            with open(self.filename_metawords, "w") as f:
                writer = csv.writer(f)
                writer.writerow(["id", "count", "word"])
  
    def update_list(self, set_of_words: set()) -> None:
        for word in set_of_words:
            self._update_or_add_word(word, self.filename_metawords)
                
    def _update_or_add_word(self, word_to_update_or_add: str, file: typing.TextIO) -> None:
        lines = []
        with open(self.filename_metawords, "r") as file:
            reader = csv.reader(file)
            lines = list(reader)
            word_updated = False
            for line in lines:
                if line[2] == word_to_update_or_add:
                    count = line[1]
                    count = str(int(count) + 1)
                    line[1] = count
                    word_updated = True
            if word_updated is False:
                lines.append(["id", 1, word_to_update_or_add])
        
        with open(self.filename_metawords, "w") as file:
            writer = csv.writer(file)
            writer.writerows(lines)
        
                