import lxml
import pyperclip
import json
import html
import spacy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.actionbar import ActionBar
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from kivy.properties import ListProperty, StringProperty, ObjectProperty, AliasProperty
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


class MessageBox(Popup):
    def popup_dismiss(self):
        self.dismiss()
        
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """
    selected_value = StringProperty('')
    
class SelectableButton(RecycleDataViewBehavior, Button):
    """Kivy widget that shows a fuzzy search match"""
    index = None

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_press(self):
        self.parent.selected_value = 'Selected: {}'.format(self.text)

    def on_release(self):
        MessageBox().open()
        
class FuzzySearchResultsRV(RecycleView):
    """Kivy widget that shows a list of fuzzy search matches"""
    fuzzy_search_matches = ObjectProperty()

    def __init__(self, **kwargs):
        super(FuzzySearchResultsRV, self).__init__(**kwargs)
        self.data = [{'text': x} for x in ["grocery", "airplane"]]

class DeletableButton(RecycleDataViewBehavior, Button):
    """Kivy widget that shows a deletable category (NOT WORKING RN)"""
    # TODO: this thing ain't working...self.text is not linked to the data in CategoryLabelsRV
    index = None

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(DeletableButton, self).refresh_view_attrs(rv, index, data)

    def on_press(self):
        self.parent.selected_value = 'Selected: {}'.format(self.text)

    def on_release(self):
        MessageBox().open()
         
class CategoryLabelsRV(RecycleView):
    """Kivy widget that shows a list of categories"""
    category_labels = ObjectProperty()

    def __init__(self, **kwargs):
        super(CategoryLabelsRV, self).__init__(**kwargs)
        self.data = [{'text': x} for x in ["job posting", "mock data", "news article"]]
             
class ProcessHtml(BoxLayout):
    html_input = ObjectProperty()
    html_output = ObjectProperty()
    url = ObjectProperty()
    category_labels = ObjectProperty()
    
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
    
    def clear_all_saved_data(self):
        # CAREFUL: this will delete even the original html backed up on disk
        object_builder.clear_all_files(original_html=True)
        self.html_output.text = "All data saved on disk by this application was erased"
        
    def fuzzy_search_related_categories(self):
        pass
        
    

class UI(App):
    Window.maximize() 
    pass


if __name__ == '__main__':
    UI().run()