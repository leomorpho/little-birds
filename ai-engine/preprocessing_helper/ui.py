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
from preprocessing.html_parsers import HtmlCleaner
from preprocessing.object_builder import pretty_clean, pipeline_result
import json
import html
import spacy

# Take raw scraped html and clean it, giving it back through clipboard.
# if args.pretty:
#     clean_html

# Remove all javascript
# Remove html comments
# Change new lines and longer than 1 space to 1 space
# Encode

   
html_cleaner = HtmlCleaner()

class ProcessHtml(BoxLayout):
    html_input = ObjectProperty()
    html_output = ObjectProperty()
    
    def pretty_clean(self):
        if self.html_input.text == "":
            return
        self.html_output.text = pretty_clean(self.html_input.text)
        pyperclip.copy(self.html_output.text)
        pyperclip.paste()
    
    # Go from raw to ready for addition to training corpus
    def pipeline(self):
        if self.html_input.text == "":
            return
        result = pipeline_result(self.html_input.text)
        self.html_output.text = json.dumps(result, indent=4)
        # pyperclip.copy(self.html_output.text)
        # pyperclip.paste()
        
    

class Ui(App):
    Window.maximize() 
    pass


if __name__ == '__main__':
    Ui().run()