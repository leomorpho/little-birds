import uuid
import html
import os
import logging
import json
import jsonlines
import config
from src.parser.html_ingester import bare_html, CustomHtmlTarget
from src.iadp.csv_db import MetaWordsImprover
from bs4 import BeautifulSoup as bs
from typing import List, Dict
from lxml import etree
from .nlp.constants_en import META_WORDS_OF_INTEREST

log = logging.getLogger()
log.setLevel(config.LOG_LEVEL)

# Keys of the filenames dictionanry holding all of the filenames constants
OUTPUT_FOLDER_KEY = "output_folder_key"
CORPUS_FILENAME_KEY = "corpus_filename_key"
SOURCE_HTML_FILENAME_KEY = "source_html_filename_key"
METAWORDS_FILENAME_KEY = "metawords_filename_key"

# Filenames dictionnary holding all of the filenames constants.
# The set values are defaults and can be overriden.
filenames = {OUTPUT_FOLDER_KEY: "output",
             CORPUS_FILENAME_KEY: "corpus.jsonl",  # output of program
             SOURCE_HTML_FILENAME_KEY: "source_html.jsonl",  # original input of program
             METAWORDS_FILENAME_KEY: "metawords.csv"}  # words form html tags

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
    clean_html = bare_html(html_str)
    soup = bs(clean_html, "html.parser")
    return soup.prettify()


def pprint_unescape(escaped_html_str: str) -> str:
    unescaped = html.unescape(escaped_html_str)
    soup = bs(unescaped, "html.parser")
    return soup.prettify()


def call_pipeline(html_str: str, url: str = None) -> str:
    log.info("Enter call pipeline")
    raw_html = bare_html(html_str)
    parser = etree.HTMLParser(
        target=CustomHtmlTarget(),
        remove_blank_text=True,
        remove_comments=True,
        remove_pis=True)
    result = etree.HTML(raw_html, parser)

    # The following is not efficient, but lxml parser keeps adding root tags
    # (html, body) to "incomplete" html strings. Since I only want to preserve
    #  the original, this is not ok, and I use a different parser to get the
    # clean raw html. Since I only save the raw html for my corpus, the expense
    # is not that significant...
    raw_html = html.escape(" ".join(raw_html.split()))
    raw_html = ' '.join(raw_html.split())

    uuid_str = str(uuid.uuid4())
    original_text = " ".join(result.full_text)
    concise_text = " ".join(result.short_text)

    # Persist words of interest to DB to sort them by prevalence and select new good ones
    # to add to META_WORDS_OF_INTEREST and USELESS_HTML_ATTRS_CONSTANTS
    meta_words_of_interest = result.meta_words_of_interest
    meta_words_improver = MetaWordsImprover(METAWORDS_FILEPATH)
    meta_words_improver.update_list(meta_words_of_interest)
    # meta_words_improver.update_list(meta_words_of_interest)

    meta_words_of_interest = list(
        meta_words_of_interest & META_WORDS_OF_INTEREST)
    meta = result.meta

    # log.debug(original_text)
    # log.debug(concise_text)
    obj = {
        "id": uuid_str,
        "url": url,
        "text": original_text,
        "conscise_text": concise_text,
        "meta_words_of_interest": meta_words_of_interest,
        # "meta": meta,
        "annotation_approver": [],
        "labels": [],
        "html": raw_html
    }
    log.info("Exit call pipeline")
    return obj


def clear_all_files(original_html=False) -> None:
    if original_html:
        files = [SOURCE_HTML_FILEPATH, CORPUS_FILEPATH, METAWORDS_FILEPATH]
    else:
        files = [CORPUS_FILEPATH, METAWORDS_FILEPATH]
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

    with jsonlines.open(SOURCE_HTML_FILEPATH, mode="r") as reader:
        for obj in reader:
            html_str = html.unescape(obj["escaped_html"])
            pipeline_and_save(html_str=html_str, write_mode="w",
                              persist_original_html=False)


def pipeline_and_save(html_str: str,
                      write_mode: str = "r",
                      url: str = None,
                      persist_original_html: bool = True
                      ) -> None:
    # Add button in UI to save html (with url) to DB. Should there also be an option
    # to add words to the metawords (like handpicked categories). This option would
    # need autocomplete to be sure not to create too many metawords
    if not html_str:
        raise ValueError("pipeline cannot run on empty string")

    # output folder must be set before calling pipeline because metawords
    # are written to it.
    if os.path.isdir(filenames["output_folder_key"]) is False:
        os.mkdir(filenames["output_folder_key"])

    result = call_pipeline(html_str, url)
    result_json = json.dumps(result, ensure_ascii=False)
    # original_html_json = json.dumps({"escaped_html": html.escape(html_str)}, ensure_ascii=False)

    if os.path.exists(CORPUS_FILEPATH) is False:
        log.info("creating corpus file")
        open(CORPUS_FILEPATH, "w").close()
    if os.path.exists(SOURCE_HTML_FILEPATH) is False:
        log.info("creating source html file")
        open(SOURCE_HTML_FILEPATH, "w").close()

    # Do not persist original html if pipeline is simply re-run on saved html
    if persist_original_html:
        # Do not overwrite SOURCE_HTML_FILEPATH or all original html data will be LOST!
        with jsonlines.open(SOURCE_HTML_FILEPATH, mode="a") as writer:
            writer.write({"escaped_html": result["html"]})
            log.info("source html saved to file")
    with jsonlines.open(CORPUS_FILEPATH, mode="a") as writer:
        writer.write(result)
        log.info("processed corpus saved to file")

    return result_json
