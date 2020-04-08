import lxml
import pyperclip
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from lxml.html.clean import Cleaner
from bs4 import BeautifulSoup as bs
import json
import uuid
import html


# Take raw scraped html and clean it, giving it back through clipboard.
# if args.pretty:
#     clean_html

# Remove all javascript
# Remove html comments
# Change new lines and longer than 1 space to 1 space
# Encode

class HtmlMetadataParser(html.parser.HTMLParser):
    """Parser implementation to extract metadata from within html tags"""
    
    tags = list()
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            self.tags.append([tag, attr])
            
            
class HtmlTextParser(html.parser.HTMLParser):
    text = ""
    def handle_data(self, data):
        print(data)
        data = data.strip()
        for i in data:
            if i.isalnum():
                self.text += data + "\n"
            break
        
                    
class HtmlCleaner():
    def pretty_clean(self, html_str):
        cleaner = Cleaner(style=True, 
                          inline_style=True, 
                          links=False, 
                          page_structure=False)
        clean_html = cleaner.clean_html(html_str)
        soup = bs(clean_html)  
        return soup.prettify()
    
    def full_clean(self, html_str):
        cleaner = Cleaner(style=True, 
                          inline_style=True, 
                          links=False, 
                          page_structure=True)
        clean_html = cleaner.clean_html(html_str)
        clean_html = " ".join(clean_html.split())
        clean_html = html.escape(clean_html)
        return clean_html
    
    def extract_data_in_place(self, html_str):
        html_str = html.unescape(html_str)
        soup = bs(html_str)  
        text = soup.get_text()
        return text
    
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
        clean_html = cleaner.clean_html(html_str)
        # clean_html = clean_html.replace("\n", "")
        # clean_html = clean_html.strip()
        # clean_html = " ".join(clean_html.split())
        meta = self.get_html_meta(html_str)
        text = self.extract_and_format_text(clean_html)
        # soup = bs(html_str)  
        # text = soup.get_text()
        result = {
            "id": str(uuid.uuid4()),
            "text": text,
            "html": html_str,
            "meta": meta,
            "annotation_approver": None, 
            "labels": []
        }
        return result
    
    def get_html_meta(self, html_str):
        parser = HtmlMetadataParser()
        parser.feed(html_str)
        result = parser.tags
        return result
    
    def extract_and_format_text(self, html_str):
        parser = HtmlTextParser()
        parser.feed(html_str)
        result = parser.text
        return result
   
html_cleaner = HtmlCleaner()

class ProcessHtml(BoxLayout):
    html_input = ObjectProperty()
    html_output = ObjectProperty()
    
    def pretty_clean(self):
        if self.html_input.text == "":
            return
        self.html_output.text = html_cleaner.pretty_clean(self.html_input.text)
        pyperclip.copy(self.html_output.text)
        pyperclip.paste()
    
    def deep_clean(self):
        if self.html_input.text == "":
            return
        self.html_output.text = html_cleaner.full_clean(self.html_input.text)
        pyperclip.copy(self.html_output.text)
        pyperclip.paste()
    
    def extract_data_in_place(self):
        if self.html_input.text == "":
            return
        text = html_cleaner.extract_data_in_place(self.html_input.text)
        
        self.html_output.text = ""
    
    # Go from raw to ready for addition to training corpus
    def pipeline(self):
        if self.html_input.text == "":
            return
        result = html_cleaner.pipeline_result(self.html_input.text)
        self.html_output.text = json.dumps(result, indent=4)
        # pyperclip.copy(self.html_output.text)
        # pyperclip.paste()
        
    

class UserInterface(App):
    Window.maximize() 
    pass


if __name__ == '__main__':
    UserInterface().run()