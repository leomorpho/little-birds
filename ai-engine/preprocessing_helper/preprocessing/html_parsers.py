import html
from html.parser import HTMLParser
from lxml.html.clean import Cleaner

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
IGNORE_CHARS = {"/n", " "}


class CustomHtmlParser(HTMLParser):
    meta = list()
    text = []
    def handle_data(self, data):
        data = data.strip()
        for i in data:
            if i not in IGNORE_CHARS:
                if self.get_starttag_text()[1:-1] in NEWLINE_ELEMENTS:
                    self.text += data + "\n"
                else:
                    self.text += " " + data
            break
  
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            self.meta.append([tag, attr])
        if tag in SEMANTIC_ELEMENTS:
            self.text += "<" + tag + ">"
    
    def handle_endtag(self, tag):
        if tag in SEMANTIC_ELEMENTS:
            self.text += "</" + tag + ">"
                
            

class HtmlCleaner():
    def pretty_clean(self, html_str):
        cleaner = Cleaner(style=True, 
                          inline_style=True, 
                          links=False, 
                          page_structure=False)
        clean_html = cleaner.clean_html(html_str)
        return clean_html
    
    def bare_html(self, html_str):
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