import pytest
import html
import os
import json
import logging
import config
from shutil import rmtree
from src.html_parsers import HtmlCleaner
from ..object_builder import update_files_and_folders, pipeline_and_save, clear_all_files
from ..object_builder import OUTPUT_FOLDER_KEY
from ..object_builder import get_filepaths_list

log = logging.getLogger()
log.setLevel(config.LOG_LEVEL)

TESTDATA_FILEPATH = "src/tests/test_data/elements.txt"
OUTPUT_FOLDER = "tmp"
FILEPATHS = []

# Used to clean raw html
cleaner = HtmlCleaner()

def open_test_data(path):
    with open(path, "r") as f:
        return f.readlines()

@pytest.fixture
def manage_filepaths():
    # Creates the directories and files needed for a test
    paths = dict()
    # Update OUTPUT_FOLDER to be a tmp folder
    paths[OUTPUT_FOLDER_KEY] = OUTPUT_FOLDER
    update_files_and_folders(paths)
    # Get updated filepaths with new main directory
    global FILEPATHS
    FILEPATHS = get_filepaths_list()
    yield
    # Teardown
    rmtree(OUTPUT_FOLDER)

class TestPipelineAndSave():
    def verify_files_were_created(self):
        for path in FILEPATHS:
            assert(os.path.exists(path) is True) 
    
    def verify_cleared_files_empty(self):
        for path in FILEPATHS:
            try:
                assert(os.stat(path).st_size == 0)
            except FileNotFoundError:
                pass
    
    def verify_all_files_gone(self):
        for path in FILEPATHS:
            assert(os.path.exists(path) is False)
    
    def test_well_formed_html_disk(self, manage_filepaths):
        self.verify_all_files_gone()
        raw_html_lines = open_test_data(TESTDATA_FILEPATH)
        for raw_html_line in raw_html_lines:
            unescaped_html = html.unescape(raw_html_line)
            result = pipeline_and_save(unescaped_html, "w")
            assert(result is not None)
        self.verify_files_were_created()
        clear_all_files()
        self.verify_cleared_files_empty()
        
    def test_empty_html(self):
        self.verify_all_files_gone()
        with pytest.raises(ValueError):
            _ = pipeline_and_save("", "w")
        self.verify_cleared_files_empty()
    
    class TestCase():
        def __init__(self, 
                     test_case_name,
                     raw_html, 
                     text, 
                     unprocessed_text, 
                     meta_words_of_interest=[],
                     meta=[],
                     annotation_approver=[],
                     labels=[]):
            self.test_case_name = test_case_name
            self.raw_html = raw_html
            self.text = text
            self.unprocessed_text = unprocessed_text
            self.escaped_html_src = html.escape(cleaner.bare_html(raw_html))
            self.meta_words_of_interest = meta_words_of_interest
            self.meta = meta
            self.annotation_approver = annotation_approver
            self.labels = labels
            
     
    # <br/> is added if a tag is a newline tag (div, article...)       
    table_test = [TestCase("price",
                            raw_html='<div>$42</div>', # divs will be removed
                            text="$42 <br/>",
                            unprocessed_text="$42 <br/>"),
                  TestCase("price with punctuation",
                            raw_html='!"#%&\'()*+,-./:;<=>?@[\\]^_`{|}~price: $42', # time won't be removed
                            text="price $42",
                            unprocessed_text="price $42"),
                  TestCase("simple word",
                            raw_html="hello",
                            text="hello",
                            unprocessed_text="hello"),
                  TestCase("non-words",
                            raw_html="uanjrgd oierjg",
                            text="",
                            unprocessed_text=""),
                  TestCase("numbers",
                            raw_html="42",
                            text="42",
                            unprocessed_text="42"),
                  TestCase("numbers",
                            raw_html="43 42",
                            text="43 42",
                            unprocessed_text="43 42"),
                  TestCase("simple div",
                            raw_html="<div>simple</div>",
                            text="simple <br/>",
                            unprocessed_text="simple <br/>"),
                  TestCase("simple div with non-words",
                            raw_html="<div>simple negfn-winkjsrgnds</div>",
                            text="simple <br/>",
                            unprocessed_text="simple <br/>"),
                  TestCase("contraction",
                            raw_html="<time>can't shan't won't don't</time>",
                            text="<time> can not shall not will not do not </time>",
                            unprocessed_text="<time> can't shan't won't don't </time>"),
                  TestCase("meta words",
                            raw_html="<time class=\"aSmallTree\">is furious</time>",
                            text="<time> is furious </time>",
                            unprocessed_text="<time> is furious </time>",
                            meta_words_of_interest=["small", "tree"]),
                  ]  
   
    @pytest.mark.parametrize("obj", table_test)
    def test_html_cases(self, obj, manage_filepaths):
        self.verify_all_files_gone()
        log.info(f"### TESTCASE {obj.test_case_name}: \"{obj.raw_html}\"")
        result = pipeline_and_save(obj.raw_html, "w")
        assert(result is not None)
        result = json.loads(result)
        assert(result["id"] is not None)
        assert(result["text"] == obj.text)
        assert(result["full_text"] == obj.unprocessed_text)
        assert(result["id"] != "")
        for word in result["meta_words_of_interest"]:
            assert(word in obj.meta_words_of_interest)
        # assert(len(result["meta"]) == len(obj.meta))
        assert(len(result["annotation_approver"]) == len(obj.annotation_approver))
        assert(len(result["labels"]) == len(obj.labels))
        assert(result["html"] == obj.escaped_html_src)
        self.verify_files_were_created()
        clear_all_files()
        self.verify_cleared_files_empty()
        