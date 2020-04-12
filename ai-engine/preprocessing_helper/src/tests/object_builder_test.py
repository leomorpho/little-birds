import pytest
import html
import os
from ..object_builder import update_files_and_folders, pipeline_and_save, clear_all_files
from ..object_builder import CORPUS_FILEPATH, SOURCE_HTML_FILEPATH, METAWORDS_FILEPATH

TESTDATA_FILEPATH = "src/tests/test_data/elements.txt"
OUTPUT_FOLDER = "tmp"

PATHS_TO_CHECK = [OUTPUT_FOLDER, 
                  CORPUS_FILEPATH, 
                  SOURCE_HTML_FILEPATH, 
                  METAWORDS_FILEPATH]

def open_test_data():
    with open(TESTDATA_FILEPATH, "r") as f:
        return f.readlines()

@pytest.fixture
def set_dirs_and_files():
    # Creates the directories and files needed for a test
    paths = dict()
    # Update OUTPUT_FOLDER to be a tmp folder
    paths["OUTPUT_FOLDER"] = OUTPUT_FOLDER
    update_files_and_folders(paths)

class TestPipelineAndSave():
    def verify_files_were_created(self):
        for path in PATHS_TO_CHECK:
            assert(os.path.exists(path) is True) 
    
    def verify_all_files_gone(self):
        for path in PATHS_TO_CHECK:
            assert(os.path.exists(path) is False)
    
    def test_well_formed_html(self, set_dirs_and_files):
        self.verify_all_files_gone()
        raw_html_lines = open_test_data()
        for raw_html_line in raw_html_lines:
            unescaped_html = html.unescape(raw_html_line)
            result = pipeline_and_save(unescaped_html, "w")
            assert(result is not None)
        self.verify_files_were_created()
        clear_all_files()
        self.verify_all_files_gone()
        
    
    def test_empty_html(self, set_dirs_and_files):
        self.verify_all_files_gone()
        with pytest.raises(ValueError):
            _ = pipeline_and_save("", "w")
        self.verify_all_files_gone()
