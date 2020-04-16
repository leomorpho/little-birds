import config
import logging
import pytest
import string
from ..nlp import nlp

log = logging.getLogger()
log.setLevel(config.LOG_LEVEL)

class InputOutputTestCase():
    """Default input output test case"""
    def __init__(self, name, input, expected_output):
        self.name = name
        self.input = input
        self.expected_output = expected_output
            
class TestNlpHelpers():
    class SplitWordsTestCase():
        """Default input output test case"""
        def __init__(self, name, input, expected_output, str_type):
            self.name = name
            self.input = input
            self.str_type = str_type
            self.expected_output = expected_output
        
    ##########################################
    ##########################################
    # Word splitting tests
    ##########################################
    ##########################################
    #NOTE: the nlp tests must not edit the html tags
    html_meta_to_split = [
        SplitWordsTestCase(
            name="Camel Case",
            input=["aCamelCaseWordToSplit"],
            str_type="html_meta",
            expected_output=["a", "Camel", "Case", "Word", "To", "Split"]),
        SplitWordsTestCase(
            name="Underscore",
            input=["a_snake_case_word_to_split"],
            str_type="html_meta",
            expected_output=["a", "snake", "case", "word", "to", "split"]),
        SplitWordsTestCase(
            name="Html tags",
            input=["<article></article>"],
            str_type="html_meta",
            expected_output=["<article></article>"]),
        SplitWordsTestCase(
            name="Html tags with capitals",
            input=["<arTicLe></arTicLe>"],
            str_type="html_meta",
            expected_output=["<ar", "Tic", "Le></ar", "Tic", "Le>"]),
        SplitWordsTestCase(
            name="Camel and snake Case",
            input=["aCamel_caseWord_toSplit"],
            str_type="html_meta",
            expected_output=["a", "Camel", "case", "Word", "to", "Split"]),
        SplitWordsTestCase(
            name="Camel and snake Case with $ signs",
            input=["aCamel_ca.seWord_toSplit"],
            str_type="html_meta",
            expected_output=["a", "Camel", "ca", "se", "Word", "to", "Split"]),
        SplitWordsTestCase(
            name="Contractions",
            input=["shouldn't can't musn't"],
            str_type="html_meta",
            expected_output=["shouldn't", "can't", "musn't"]),
        SplitWordsTestCase(
            name="Quotes",
            input=['"angry" "lions"'],
            str_type="html_meta",
            expected_output=['"angry"', '"lions"']),
        SplitWordsTestCase(
            name="Quotes with capitals",
            input=['"Angry" "lions"'],
            str_type="html_meta",
            expected_output=['"', 'Angry"', '"lions"'])]
    
    @pytest.mark.parametrize("case", html_meta_to_split)
    def test_html_meta_splitting_cases(self, case):
        log.info("Case: " + case.name)
        log.debug("Input: " + str(case.input))
        result = nlp.split_word(case.input[0], str_type=case.str_type)
        log.debug("Result: " + str(result))
        assert(result == case.expected_output)
    
    sentences_to_split = [
        SplitWordsTestCase(
            name="Sentence with punctuation",
            input=["word,"],
            str_type="punctuation",
            expected_output=["word", ","])]
    
    @pytest.mark.parametrize("case", sentences_to_split)
    def test_sentences_splitting_cases(self, case):
        log.info("Case: " + case.name)
        log.debug("Input: " + str(case.input))
        result = nlp.split_word(case.input[0], str_type=case.str_type)
        log.debug("Result: " + str(result))
        assert(result == case.expected_output)
    
    ##########################################
    ##########################################
    # Special chars tests
    ##########################################
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
        result = nlp.remove_chars_from_list(case.input, 
                                      acceptable_chars_list=case.acceptable_chars_list)
        log.debug("Result: " + str(result))
        assert(result == case.expected_output)
    
    ##########################################
    ##########################################
    # Expand contractions tests
    ##########################################
    ##########################################
    
    expand_contraction_cases = [
        InputOutputTestCase(
            name="nominal",
            input="can't",
            expected_output="cannot"
        ),
        InputOutputTestCase(
            name="Another",
            input="I'd",
            expected_output="I would"
        )
    ]
    @pytest.mark.parametrize("case", expand_contraction_cases)
    def test_expand_contraction(self, case):
        log.info("Case: " + case.name)
        log.debug("Input: " + str(case.input))
        result = nlp.expand_contraction(case.input)
        log.debug("Result: " + str(result))
        assert(result == case.expected_output)

    expand_contractions_in_list_cases = [
        InputOutputTestCase(
            name="nominal",
            input=["can't", "shouldn't", "couldn't"],
            expected_output=["cannot", "should", "not", "could", "not"]
        )
    ]
    @pytest.mark.parametrize("case", expand_contractions_in_list_cases)
    def test_expand_contractions_in_list(self, case):
        log.info("Case: " + case.name)
        log.debug("Input: " + str(case.input))
        result = nlp.expand_contractions_in_list(case.input)
        log.debug("Result: " + str(result))
        assert(result == case.expected_output)
 
##########################################  
##########################################
# Test restructures
########################################## 
##########################################    
class TestRestructure():
    class RestructureTestCase():
        def __init__(self, name, input, expected_output, html_meta=False):
            self.name = name
            self.input = input
            self.html_meta = html_meta
            self.expected_output = expected_output
            
    to_restructure = [
        RestructureTestCase(
            name="Nominal",
            input="This sentence needs some processing",
            html_meta=False,
            expected_output=["This", "sentence", "needs", "some", "processing"]
        ),
        RestructureTestCase(
            name="Html attribute",
            input="shortLittleClass",
            html_meta=True,
            expected_output=["short", "little", "class"]
        ),
        RestructureTestCase(
            name="Contractions",
            input="He shouldn't, she mustn't",
            html_meta=False,
            expected_output=["He", "should", "not", ",", "she", "must", "not"]
        )
    ]

    @pytest.mark.parametrize("case", to_restructure)
    def test_restructure(self, case):
        log.info("Case: " + case.name)
        log.debug("Input: " + str(case.input))
        result = nlp.restructure(case.input, case.html_meta)
        log.debug("Result: " + str(result))
        assert(result == case.expected_output)