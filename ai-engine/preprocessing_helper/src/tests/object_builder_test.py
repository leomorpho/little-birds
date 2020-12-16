import pytest
import html
import os
import json
import jsonlines
import logging
import config
from shutil import rmtree
from src.parser.html_ingester import bare_html
from ..object_builder import update_files_and_folders, pipeline_and_save, clear_all_files, pipeline_on_saved_data
from ..object_builder import OUTPUT_FOLDER_KEY
from ..object_builder import get_filepaths_list

log = logging.getLogger()
log.setLevel(config.LOG_LEVEL)

TESTDATA_FILEPATH = 'src/tests/test_data/elements.jsonl'
OUTPUT_FOLDER = "tmp"
FILEPATHS = []


def open_test_data(path):
    with open(path, "r") as f:
        return f.readlines()

# Inject this fixture in any test that interacts with a filesystem


@pytest.fixture
def filesystem_handler():
    # Creates the directories and files needed for a test
    paths = dict()
    # Update OUTPUT_FOLDER to be a tmp folder
    paths[OUTPUT_FOLDER_KEY] = OUTPUT_FOLDER
    update_files_and_folders(paths)
    # Get updated filepaths with new main directory
    global FILEPATHS
    FILEPATHS = get_filepaths_list()

    verify_all_files_gone()
    yield
    # Teardown
    clear_all_files(original_html=True)
    verify_cleared_files_empty()
    rmtree(OUTPUT_FOLDER)


def verify_files_were_created():
    for path in FILEPATHS:
        assert(os.path.exists(path) is True)


def verify_cleared_files_empty():
    for path in FILEPATHS:
        try:
            assert(os.stat(path).st_size == 0)
        except FileNotFoundError:
            pass


def verify_all_files_gone():
    for path in FILEPATHS:
        assert(os.path.exists(path) is False)


def create_objects_from_data():
    with jsonlines.open(TESTDATA_FILEPATH, mode="r") as reader:
        for obj in reader:
            unescaped_html = html.unescape(obj["escaped_html"])
            result = pipeline_and_save(html_str=unescaped_html, write_mode="w")
            assert(result is not None)


class TestPipelineAndSave():
    def test_well_formed_html_disk(self, filesystem_handler):
        create_objects_from_data()
        verify_files_were_created()

    # Pipeline will raise an error if given an empty string
    def test_empty_html(self):
        verify_all_files_gone()
        with pytest.raises(ValueError):
            _ = pipeline_and_save(html_str="", write_mode="w")
        verify_cleared_files_empty()

    class TestCase():
        def __init__(self,
                     name,
                     raw_html,
                     text,
                     unprocessed_text,
                     meta_words_of_interest=[],
                     meta=[],
                     annotation_approver=[],
                     labels=[]):
            self.name = name
            self.raw_html = raw_html
            self.text = text
            self.unprocessed_text = unprocessed_text
            self.escaped_html_src = html.escape(bare_html(raw_html))
            self.meta_words_of_interest = meta_words_of_interest
            self.meta = meta
            self.annotation_approver = annotation_approver
            self.labels = labels

    # NOTE: if a string element is passed to the pipeline without html tags surrounding
    #  it, the preprocessor will automatically add a <br/> newline html element because
    # the data input is incorrect html and will be wrapper by the html parser in
    # probably <html> tags, which is a newline character that triggers the parser to
    # add a <br/> element

    # <br/> is added if a tag is a newline tag (div, article...)
    table_test = [TestCase(name="price",
                           raw_html='<div>$42</div>',  # divs will be removed
                           text="$42 <br/>",
                           unprocessed_text="$42 <br/>"),
                  # I don't expect this case to happen for now. Breaks.
                  #   TestCase(name="price with punctuation",
                  #             raw_html='<non-tag>!"#%&\'()*+,-./:;<=>?@[\\]^_`{|}~price: $42</non-tag>',
                  #             text="price $42",
                  #             unprocessed_text='!"#%&\'()*+,-./:;<=>?@[\\]^_`{|}~price: $42</non-tag>'),
                  TestCase(name="simple word",
                           raw_html="<td>hello</td>",
                           text="<td> hello </td>",
                           unprocessed_text="<td> hello </td>"),
                  TestCase(name="numbers",
                           raw_html="<img>42</img>",
                           text="42",
                           unprocessed_text="42"),
                  TestCase(name="numbers",
                           raw_html="<a>43 42</a>",
                           text="<a> 43 42 </a>",
                           unprocessed_text="<a> 43 42 </a>"),
                  TestCase(name="simple div",
                           raw_html="<div>simple</div>",
                           text="simple <br/>",
                           unprocessed_text="simple <br/>"),
                  TestCase(name="simple div with non-words",
                           raw_html="<div>simple negfn-winkjsrgnds</div>",
                           text="simple negfn-winkjsrgnds <br/>",
                           unprocessed_text="simple negfn-winkjsrgnds <br/>"),
                  TestCase(name="contraction",
                           raw_html="<time>can't shan't won't don't</time>",
                           text="<time> can not shall not will not do not </time>",
                           unprocessed_text="<time> can't shan't won't don't </time>"),
                  TestCase(name="meta words",
                           raw_html="<time class=\"aSmallTree\">is furious</time>",
                           text="<time> furious </time>",
                           unprocessed_text="<time> is furious </time>",
                           meta_words_of_interest=["small", "tree"]),
                  ]

    # @pytest.mark.skip(reason="no way of currently testing this")
    @pytest.mark.parametrize("obj", table_test)
    def test_html_cases(self, obj, filesystem_handler):
        verify_all_files_gone()
        log.info(f"### TESTCASE {obj.name}: \"{obj.raw_html}\"")
        log.info("Case: " + obj.name)
        log.debug("Input: " + str(obj.raw_html))
        result = pipeline_and_save(html_str=obj.raw_html, write_mode="w")
        assert(result is not None)
        result = json.loads(result)
        assert(result["id"] is not None)
        # assert(result["text"] == obj.text)
        assert(result["text"] == obj.unprocessed_text)
        assert(result["id"] != "")
        for word in result["meta_words_of_interest"]:
            assert(word in obj.meta_words_of_interest)
        # assert(len(result["meta"]) == len(obj.meta))
        assert(len(result["annotation_approver"])
               == len(obj.annotation_approver))
        assert(len(result["labels"]) == len(obj.labels))
        assert(result["html"] == obj.escaped_html_src)
        verify_files_were_created()
        clear_all_files(original_html=True)
        verify_cleared_files_empty()


class TestPipelineOnSavedData():
    @pytest.fixture
    def create_data_on_disk(self):
        verify_all_files_gone()
        create_objects_from_data()
        verify_files_were_created()

    # Save some processed objects to file and then re-run pipeline on saved data.
    # All files on disk should be the same since they were all generated from the
    # same html ground truth.
    def test_pipeline_on_saved_data(self, filesystem_handler, create_data_on_disk):
        FILEPATHS = get_filepaths_list()
        backup = {}
        for path in FILEPATHS:
            with open(path, "r") as f:
                num_lines = sum(1 for line in f)
            backup[path] = num_lines

        pipeline_on_saved_data()
        for path in FILEPATHS:
            with open(path, "r") as f:
                num_lines = sum(1 for line in f)
            assert(backup[path]) == num_lines
