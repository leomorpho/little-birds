import config
import logging
import pytest
from ..nlp.utils import split_words, remove_unwanted_characters

log = logging.getLogger()
log.setLevel(config.LOG_LEVEL)

class TestNlpHelpers():
    class NLPTestCase():
        """Represents a test case with input and expected output"""
        def __init__(self, case_name, input, output):
            self.case_name = case_name
            self.input = input
            self.expected_output = output
    
    #NOTE: the nlp tests do not edit the html tags, they must remain AS IS
    to_split = [NLPTestCase("Camel Case",
                                ["<div>aCamelCaseWordToSplit"],
                                ["<div>", "a", "Camel", "Case", "Word", "To", "Split",  "</div>"]),
                 NLPTestCase("Underscore",
                                ["<div>a_camel_case_word_to_split</div>"],
                                ["<div>", "a", "camel", "case", "word", "to", "split", "</div>"]),
                 NLPTestCase("Html tags",
                                ["<article></article>"],
                                ["<article></article>"]),
                 NLPTestCase("Html tags",
                                ["<arTicLe></arTicLe>"],
                                ["<arTicLe></arTicLe>"])]
    
    @pytest.mark.parametrize("case", to_split)
    def test_splitting_cases(self, case):
        assert(split_words(case.input) == case.expected_output)
        
    remove_unwanted_chars = [NLPTestCase("Nominal",
                                         ['''<div>!()-[]{};:'"\,<>./?@#$%^&*_~</div>'''],
                                         ["<div>", "</div>"])]
    
    @pytest.mark.parametrize("case", remove_unwanted_chars)
    def test_remove_unwanted_chars(self, case):
        assert(remove_unwanted_characters(case.input) == case.expected_output)