import config
import logging
import pytest
from ..nlp.utils import split_words

log = logging.getLogger()
log.setLevel(config.LOG_LEVEL)

class TestNlpHelpers():
    class NLPTestCase():
        """Represents a test case with input and expected output"""
        def __init__(self, case_name, input, output):
            self.case_name = case_name
            self.input = input
            self.expected_output = output
        
    sentences = [NLPTestCase("Camel Case",
                                ["aCamelCaseWordToSplit"],
                                ["a", "Camel", "Case", "Word", "To", "Split"]),
                 NLPTestCase("Underscore",
                                ["a_camel_case_word_to_split"],
                                ["a", "camel", "case", "word", "to", "split"])]
    
    @pytest.mark.parametrize("case", sentences)
    def test_splitting_cases(self, case):
        assert(split_words(case.input) == case.expected_output)