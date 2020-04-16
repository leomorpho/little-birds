import uuid
import html
import os
import logging
import json
import config
from src.parser.html_ingester import HtmlCleaner, CustomHtmlTarget
from src.iadp.csv_db import MetaWordsImprover
from bs4 import BeautifulSoup as bs
from typing import List, Dict
from lxml import etree
from .nlp.constants_en import META_WORDS_OF_INTEREST

log = logging.getLogger()
log.setLevel(config.LOG_LEVEL)

cleaner = HtmlCleaner()

# Keys of the filenames dictionanry holding all of the filenames constants
OUTPUT_FOLDER_KEY = "output_folder_key"
CORPUS_FILENAME_KEY = "corpus_filename_key"
SOURCE_HTML_FILENAME_KEY = "source_html_filename_key"
METAWORDS_FILENAME_KEY = "metawords_filename_key"

# Filenames dictionnary holding all of the filenames constants.
# The set values are defaults and can be overriden.
filenames = {OUTPUT_FOLDER_KEY: "output",
            CORPUS_FILENAME_KEY: "corpus.jsonl", # output of program
            SOURCE_HTML_FILENAME_KEY: "source_html.json", # original input of program
            METAWORDS_FILENAME_KEY: "metawords.csv"} # words form html tags

SOURCE_HTML_FILEPATH = filenames[OUTPUT_FOLDER_KEY] + \
    "/" + filenames[SOURCE_HTML_FILENAME_KEY]
CORPUS_FILEPATH = filenames[OUTPUT_FOLDER_KEY] + \
    "/" + filenames[CORPUS_FILENAME_KEY]
METAWORDS_FILEPATH = filenames[OUTPUT_FOLDER_KEY] + \
    "/" + filenames[METAWORDS_FILENAME_KEY]
 
def update_files_and_folders(paths: Dict[str, str]) -> None:
    """Setup files and folders names for calls from external parts (main, tests...)"""
    for key, value in paths.items():
        global filenames
        if filenames[key]:
            filenames[key] = value
    global SOURCE_HTML_FILEPATH, CORPUS_FILEPATH, METAWORDS_FILEPATH
    SOURCE_HTML_FILEPATH = filenames[OUTPUT_FOLDER_KEY] + \
        "/" + filenames[SOURCE_HTML_FILENAME_KEY]
    CORPUS_FILEPATH = filenames[OUTPUT_FOLDER_KEY] + \
        "/" + filenames[CORPUS_FILENAME_KEY]
    METAWORDS_FILEPATH = filenames[OUTPUT_FOLDER_KEY] + \
        "/" + filenames[METAWORDS_FILENAME_KEY]
        
    log.debug(f"{OUTPUT_FOLDER_KEY} set to {filenames[OUTPUT_FOLDER_KEY]}")
    log.debug(f"SOURCE_HTML_FILEPATH: {SOURCE_HTML_FILEPATH}")
    log.debug(f"CORPUS_FILEPATH: {CORPUS_FILEPATH}")
    log.debug(f"METAWORDS_FILEPATH: {METAWORDS_FILEPATH}")

def get_filepaths_list() -> List[str]:
    """Returns a list of all filepaths that are written to"""
    return [SOURCE_HTML_FILEPATH, CORPUS_FILEPATH, METAWORDS_FILEPATH]

def pretty_clean(html_str: str) -> str:
    clean_html = cleaner.pretty_clean(html_str)
    soup = bs(clean_html, "html.parser")  
    return soup.prettify()

def pprint_unescape(escaped_html_str: str) -> str:
    unescaped = html.unescape(escaped_html_str)
    soup = bs(unescaped, "html.parser")
    return soup.prettify()
    
def call_pipeline(html_str: str) -> str:
    log.info("Enter call pipeline")
    parser = etree.HTMLParser(
        target=CustomHtmlTarget(), 
        remove_blank_text=True,
        remove_comments=True,
        remove_pis=True)
    result = etree.HTML(html_str, parser)
    
    # The following is not efficient, but lxml parser keeps adding root tags 
    # (html, body) to "incomplete" html strings. Since I only want to preserve
    #  the original, this is not ok, and I use a different parser to get the 
    # clean raw html. Since I only save the raw html for my corpus, the expense
    # is not that significant...
    raw_html = cleaner.bare_html(html_str)
    raw_html = html.escape(" ".join(raw_html.split()))
    
    uuid_str = str(uuid.uuid4())
    log.info("short_text: " + str(result.short_text))
    short_text = " ".join(result.short_text)
    full_text = " ".join(result.full_text)
    
    # Persist words of interest to DB to sort them by prevalence and select new good ones
    # to add to META_WORDS_OF_INTEREST and USELESS_HTML_ATTRS_CONSTANTS
    meta_words_of_interest = result.meta_words_of_interest
    meta_words_improver = MetaWordsImprover(METAWORDS_FILEPATH)
    meta_words_improver.update_list(meta_words_of_interest)
    # meta_words_improver.update_list(meta_words_of_interest)
    
    meta_words_of_interest = list(meta_words_of_interest & META_WORDS_OF_INTEREST)
    meta = result.meta
        
    obj = {
        "id": uuid_str,
        "text": short_text,
        "full_text": full_text,
        "meta_words_of_interest": meta_words_of_interest,
        "meta": meta,
        "annotation_approver": [], 
        "labels": [],
        "html": raw_html
    }
    log.info("Exit call pipeline")
    return obj

def clear_all_files() -> None:
    files = [SOURCE_HTML_FILEPATH, CORPUS_FILEPATH, METAWORDS_FILEPATH]
    for f in files:
        open(f, "w").close()
    
def pipeline_on_saved_data() -> None:
    # Add button in UI to save html (with url) to DB. Should there also be an option 
    # to add words to the metawords (like handpicked categories). This option would 
    # need autocomplete to be sure not to create too many metawords
    if os.path.exists(SOURCE_HTML_FILEPATH) is False or os.stat(SOURCE_HTML_FILEPATH).st_size == 0:
        log.error("No saved data to run pipeline on...")
        raise Exception("No saved data to run pipeline on...")
    
    clear_all_files()
    
    original_htmls: List[str] = []
    with open(SOURCE_HTML_FILEPATH, "r") as f:
        original_htmls = f.readlines()
    
    for html in original_htmls:
        pipeline_and_save(html, "w")

def pipeline_and_save(html_str: str, write_mode :str="r") -> None:
    # Add button in UI to save html (with url) to DB. Should there also be an option 
    # to add words to the metawords (like handpicked categories). This option would 
    # need autocomplete to be sure not to create too many metawords
    if html_str is None or html_str == "":
        raise ValueError("pipeline cannot run on empty string")
    
    # output folder must be set before calling pipeline because metawords 
    # are written to it.
    if os.path.isdir(filenames["output_folder_key"]) is False:
        os.mkdir(filenames["output_folder_key"])
        
    result = call_pipeline(html_str)
    result_json = json.dumps(result, indent=4)
    
    if os.path.exists(CORPUS_FILEPATH) is False:
        log.info("creating corpus file")
        open(CORPUS_FILEPATH, "w").close()
    if os.path.exists(SOURCE_HTML_FILEPATH) is False:
        log.info("creating source html file")
        open(SOURCE_HTML_FILEPATH, "w").close()
    
    # Do not overwrite SOURCE_HTML_FILEPATH or all original html data will be LOST!
    with open(SOURCE_HTML_FILEPATH, "a+") as f:
        f.write(html.escape(html_str))
        log.info("source html saved to file")
    with open(CORPUS_FILEPATH, write_mode) as f:
        f.write(result_json)
        log.info("processed corpus saved to file")
    
    return result_json