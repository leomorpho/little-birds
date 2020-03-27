import lxml
import argparse
import pyperclip
from lxml.html.clean import Cleaner

parser = argparse.ArgumentParser(description='Clean up scraped html')
parser.add_argument("html", type=str, help="a dirty html string")
parser.add_argument("-p", "--pretty", type=bool, default=False, help="leave pretty")
args = parser.parse_args()



clean_html = ""

# Take raw scraped html and clean it, giving it back through clipboard.
if args.pretty:
    clean_html

# Remove all javascript
# Remove html comments
# Change new lines and longer than 1 space to 1 space
# Encode

class HtmlCleaner():
    def __init__(self, html, pretty):
        """
        """
        self.pretty = pretty
        self.html = html
        self.cleaner = Cleaner()
        self.cleaner.javascript = True # This is True because we want to activate the javascript filter
        self.cleaner.style = True      # This is True because we want to activate the styles & stylesheet filter
    
    def clean(self):
        if self.pretty:
            self.pretty_clean()
        else:
            self.full_clean()
    
    def pretty_clean(self):
        self.html = self.clean_javascript()
    
    def full_clean(self):
        pass
    
    def clean_spaces(self):
        pass
    
    def clean_javascript(self):
        pass
    
    def clean_html_comments(self):
        pass

htmlCleaner = HtmlCleaner(html=args.html, pretty=args.pretty)
pyperclip.copy(htmlCleaner.html)
pyperclip.paste()