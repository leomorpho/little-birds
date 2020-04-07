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
import html


# Take raw scraped html and clean it, giving it back through clipboard.
# if args.pretty:
#     clean_html

# Remove all javascript
# Remove html comments
# Change new lines and longer than 1 space to 1 space
# Encode

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
    
    def unescape(self, html_str):
        html_str = html.unescape(html_str)
        soup = bs(html_str)  
        return soup.prettify()
    
    def unescape_dumped_text(self, html_str):
        html_str = html.unescape(html_str)
        soup = bs(html_str)  
        text = soup.get_text()
        return text
   
html_cleaner = HtmlCleaner()

class ProcessHtml(BoxLayout):
    html_input = ObjectProperty()
    html_output = ObjectProperty()
    
    def pretty_clean(self):
        if self.html_input.text != "":
            self.html_output.text = html_cleaner.pretty_clean(self.html_input.text)
        pyperclip.copy(self.html_output.text)
        pyperclip.paste()
    
    def deep_clean(self):
        if self.html_input.text != "":
            self.html_output.text = html_cleaner.full_clean(self.html_input.text)
        pyperclip.copy(self.html_output.text)
        pyperclip.paste()
        
    def unescape(self):
        if self.html_input.text != "":
            self.html_output.text = html_cleaner.unescape(self.html_input.text)
    
    def unescape_dumped_text(self):
        text = ""
        if self.html_input.text != "":
            text = html_cleaner.unescape_dumped_text(self.html_input.text)
        self.html_output.text = text

class UserInterface(App):
    Window.maximize() 
    pass


if __name__ == '__main__':
    UserInterface().run()