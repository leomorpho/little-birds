import pytest
import html
from ..object_builder import update_files_and_folders, pipeline_and_save

TESTDATA_FILEPATH = "src/tests/test_data/elements.txt"

def open_test_data():
    with open(TESTDATA_FILEPATH, "r") as f:
        return f.readlines()

@pytest.fixture
def set_dirs_and_files():
    # Creates the directories and files needed for a test
    paths = dict()
    paths["OUTPUT_FOLDER"] = "tmp"
    update_files_and_folders(paths)

class TestPipelineAndSave():
    def test_well_formed_html(self, set_dirs_and_files):
        raw_html_lines = open_test_data()
        for raw_html_line in raw_html_lines:
            unescaped_html = html.unescape(raw_html_line)
            result = pipeline_and_save(unescaped_html, "w")
            assert(result is not None)
    
    def test_empty_html(self, set_dirs_and_files):
        with pytest.raises(ValueError):
            _ = pipeline_and_save("", "w")
