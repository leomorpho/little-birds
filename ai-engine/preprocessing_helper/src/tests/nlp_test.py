import config
import logging
import pytest
import string
from ..nlp.nlp  import split_word, remove_chars_from_word

log = logging.getLogger()
log.setLevel(config.LOG_LEVEL)

class TestNlpHelpers():
    class NLPTestCase():
        """Represents a test case with input and expected expected_output"""
        def __init__(self, name, input, expected_output):
            self.name = name
            self.input = input
            self.expected_output = expected_output
    
    #NOTE: the nlp tests must not edit the html tags
    to_split = [NLPTestCase("Camel Case",
                                ["aCamelCaseWordToSplit"],
                                ["a", "Camel", "Case", "Word", "To", "Split"]),
                 NLPTestCase("Underscore",
                                ["a_snake_case_word_to_split"],
                                ["a", "snake", "case", "word", "to", "split"]),
                 NLPTestCase("Html tags",
                                ["<article></article>"],
                                ["<article></article>"]),
                 NLPTestCase("Html tags with capitals",
                                ["<arTicLe></arTicLe>"],
                                ["<ar", "Tic", "Le></ar", "Tic", "Le>"])]
    
    @pytest.mark.parametrize("case", to_split)
    def test_splitting_cases(self, case):
        log.info("Case: " + case.name)
        log.debug("Input: " + str(case.input))
        result = split_word(case.input[0])
        log.debug("Result: " + str(result))
        assert(result == case.expected_output)
     
    all_punctuation = string.punctuation + '“'
    class SpecialCharsCase():
        """Represents a test case with input and expected expected_output"""
        def __init__(self, name, input, expected_output, acceptable_chars_list=None):
            self.name = name
            self.input = input
            self.acceptable_chars_list = acceptable_chars_list
            self.expected_output = expected_output
    remove_unwanted_chars = [
        SpecialCharsCase(
            name="Nominal",
            input=["<div>", "!()-[]{};:'\"\,<>./?@#$%^&*_~", "</div>"],
            expected_output=["<div>", "</div>"]),
        SpecialCharsCase(
            name="Random chars",
            input=["<div>", "!()-[]", "{};:'\"\,<", ">./?@", "#$%^&*_~", "</div>"],
            expected_output=["<div>", "</div>"]),
        SpecialCharsCase(
            name="A sentence is hiding",
            input=["<div>", "!()a-[]", "{}senten;:'\"\,ce<", ">.is/?@", "#$%hi^&*ding_~", "</div>"],
            expected_output=["<div>", "a", "sentence", "is", "hiding", "</div>"]),
        SpecialCharsCase(
            name="Let's keep percent signs",
            input=["<div>", "The!()-[re", "is", ":'\"\,<a", "per:'\"\,<cent", "char", "%", "</div>"],
            acceptable_chars_list=["%"],
            expected_output=["<div>", "There", "is", "a", "percent", "char", "%", "</div>"]),
        SpecialCharsCase(
            name="All punctuation tolerated in a tolerant land",
            input=["<div>", f'''{all_punctuation}''', "</div>"],
            acceptable_chars_list=list(all_punctuation),
            expected_output=["<div>", f'''{all_punctuation}''', "</div>"])]
    
    @pytest.mark.parametrize("case", remove_unwanted_chars)
    def test_remove_unwanted_chars(self, case):
        log.info("Case: " + case.name)
        log.debug("Input: " + str(case.input))
        result = remove_chars_from_word(case.input, 
                                      acceptable_chars_list=case.acceptable_chars_list)
        log.debug("Result: " + str(result))
        assert(result == case.expected_output)