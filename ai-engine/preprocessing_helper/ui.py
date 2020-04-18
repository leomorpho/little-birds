import lxml
import pyperclip
import json
import html
import spacy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.actionbar import ActionBar
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from src.parser.html_ingester import bare_html
from src import object_builder


# Take raw scraped html and clean it, giving it back through clipboard.
# if args.pretty:
#     clean_html

# Remove all javascript
# Remove html comments
# Change new lines and longer than 1 space to 1 space
# Encode

class ProcessHtml(BoxLayout):
    html_input = ObjectProperty()
    html_output = ObjectProperty()
    url = ObjectProperty()
    
    def pretty_clean(self):
        if self.html_input.text == "":
            self.html_output.text = "You must enter html data to pretty print it"
            return
        self.html_output.text = object_builder.pretty_clean(self.html_input.text)
        # pyperclip.copy(self.html_output.text)
        # pyperclip.paste()
    
    def escape(self):
        if self.html_input.text == "":
            self.html_output.text = "You must enter html data to escape it"
            return
        self.html_output.text = html.escape(" ".join(self.html_input.text.split()))
        pyperclip.copy(self.html_output.text)
        pyperclip.paste()
        
    def pprint_unescape(self):
        if self.html_input.text == "":
            self.html_output.text = "You must enter escaped data to unescape it"
            return
        self.html_output.text = object_builder.pprint_unescape(self.html_input.text)
        # pyperclip.copy(self.html_output.text)
        # pyperclip.paste()
        
    # Format for training corpus
    def pipeline(self):
        if self.html_input.text == "":
            self.html_output.text = "You must enter html data to parse it"
            return
        result = object_builder.call_pipeline(self.html_input.text)
        self.html_output.text = json.dumps(result, indent=4)
        # pyperclip.copy(self.html_output.text)
        # pyperclip.paste()
        
    # Format for training corpus
    def pipeline_on_saved_data(self):
        try:
            object_builder.pipeline_on_saved_data()
        except Exception as err:
            self.html_output.text = str(err)
            return
        self.html_output.text = "Done! Pipeline ran on all saved items"
        # pyperclip.copy(self.html_output.text)
        # pyperclip.paste()
    
    # Format for training corpus
    def pipeline_and_save(self):
        if not self.html_input.text:
            self.html_output.text = "You must enter html data to parse it and save it to file"
            return
        print("HERE")
        print(self.url.text)
        if not self.url.text:
            self.html_output.text = "You must enter the url for the entered html"
            return  
        try:
            result = "Done! The following item was saved to file:\n\n"
            result += object_builder.pipeline_and_save(
                html_str=self.html_input.text, 
                url=self.url.text, 
                write_mode="a+")
            self.html_output.text = result
        except Exception as err:
            self.html_output.text = str(err)
        # pyperclip.copy(self.html_output.text)
        # pyperclip.paste()
        
    

class UI(App):
    Window.maximize() 
    pass


if __name__ == '__main__':
    UI().run()