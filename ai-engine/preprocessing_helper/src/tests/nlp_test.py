import config
import logging
import pytest
import string
from ..nlp import nlp

log = logging.getLogger()
log.setLevel(config.LOG_LEVEL)

class TestNlpHelpers():
    class InputOutputTestCase():
        """Represents a test case with input and expected expected_output"""
        def __init__(self, name, input, expected_output):
            self.name = name
            self.input = input
            self.expected_output = expected_output
    
    ##########################################
    # Word splitting tests
    ##########################################
    #NOTE: the nlp tests must not edit the html tags
    to_split = [
        InputOutputTestCase(
            name="Camel Case",
            input=["aCamelCaseWordToSplit"],
            expected_output=["a", "Camel", "Case", "Word", "To", "Split"]),
        InputOutputTestCase(
            name="Underscore",
            input=["a_snake_case_word_to_split"],
            expected_output=["a", "snake", "case", "word", "to", "split"]),
        InputOutputTestCase(
            name="Html tags",
            input=["<article></article>"],
            expected_output=["<article></article>"]),
        InputOutputTestCase(
            name="Html tags with capitals",
            input=["<arTicLe></arTicLe>"],
            expected_output=["<ar", "Tic", "Le></ar", "Tic", "Le>"]),
        InputOutputTestCase(
            name="Camel and snake Case",
            input=["aCamel_caseWord_toSplit"],
            expected_output=["a", "Camel", "case", "Word", "to", "Split"]),
        InputOutputTestCase(
            name="Camel and snake Case with $ signs",
            input=["aCamel_ca.seWord_toSplit"],
            expected_output=["a", "Camel", "ca", "se", "Word", "to", "Split"]),
        InputOutputTestCase(
            name="Contractions",
            input=["shouldn't can't musn't"],
            expected_output=["shouldn't", "can't", "musn't"]),
        InputOutputTestCase(
            name="Quotes",
            input=['"angry" "lions"'],
            expected_output=['"angry"', '"lions"']),
        InputOutputTestCase(
            name="Quotes with capitals",
            input=['"Angry" "lions"'],
            expected_output=['"', 'Angry"', '"lions"'])]
    
    @pytest.mark.parametrize("case", to_split)
    def test_splitting_cases(self, case):
        log.info("Case: " + case.name)
        log.debug("Input: " + str(case.input))
        result = nlp.split_word(case.input[0])
        log.debug("Result: " + str(result))
        assert(result == case.expected_output)
     
    ##########################################
    # Special chars tests
    ##########################################
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
        result = nlp.remove_chars_from_word(case.input, 
                                      acceptable_chars_list=case.acceptable_chars_list)
        log.debug("Result: " + str(result))
        assert(result == case.expected_output)
    
    
    ##########################################
    # Expand contractions tests
    ##########################################
    expand_contractions_cases = [
        InputOutputTestCase(
            name="nominal",
            input="can't",
            expected_output="cannot"
        )
    ]
    @pytest.mark.parametrize("case", expand_contractions_cases)
    def test_expand_contractions(self, case):
        log.info("Case: " + case.name)
        log.debug("Input: " + str(case.input))
        result = nlp.expand_contractions(case.input)
        log.debug("Result: " + str(result))
        assert(result == case.expected_output)
