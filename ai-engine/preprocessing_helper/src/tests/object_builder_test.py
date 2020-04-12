import pytest
from ..object_builder import set_files_and_folders


@pytest.fixture
def dirs_and_files():
    # Creates the directories and files needed for a test
    paths = dict()
    paths["OUTPUT_FOLDER"] = "tmp"
    set_files_and_folders(paths)

class TestPipelineAndSave():
    def test_wf_html(self, dirs_and_files):
        pass
        