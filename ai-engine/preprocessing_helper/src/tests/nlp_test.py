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
            input=["<div>", "!()-[]", "{};:'\"\,<", ">./?@",
                   "#$%^&*_~", "</div>"],
            expected_output=["<div>", "</div>"]),
        SpecialCharsCase(
            name="A sentence is hiding",
            input=["<div>", "!()a-[]", "{}senten;:'\"\,ce<",
                   ">.is/?@", "#$%hi^&*ding_~", "</div>"],
            expected_output=["<div>", "a", "sentence", "is", "hiding", "</div>"]),
        SpecialCharsCase(
            name="Let's keep percent signs",
            input=["<div>", "The!()-[re", "is", ":'\"\,<a",
                   "per:'\"\,<cent", "char", "%", "</div>"],
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
    # Remove stop words
    ##########################################
    ##########################################

    stop_word_in_list_cases = [
        InputOutputTestCase(
            name="nominal",
            input=["some", "but"],
            expected_output=[]
        ),
        InputOutputTestCase(
            name="nominal",
            input=["Beautiful", "such", "fishes", "having", "breakfast", "$"],
            expected_output=["Beautiful", "fishes", "breakfast", "$"]
        )
    ]

    @pytest.mark.parametrize("case", stop_word_in_list_cases)
    def test_remove_stop_words_from_list(self, case):
        log.info("Case: " + case.name)
        log.debug("Input: " + str(case.input))
        result = nlp.remove_stopwords_from_list(case.input)
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
        ),
        RestructureTestCase(
            name="Capitalized words",
            input="THIS WILL STAY CAPITALS",
            html_meta=False,
            expected_output=["THIS", "WILL", "STAY", "CAPITALS"]
        ),
        # RestructureTestCase(
        #     name="Punctuation",
        #     input='!"#%&\'()*+,-./:;<=>?@[\\]^_`{|}~price: $42',
        #     html_meta=False,
        #     expected_output=["price", "$42"]
        # )
    ]

    @pytest.mark.parametrize("case", to_restructure)
    def test_restructure(self, case):
        log.info("Case: " + case.name)
        log.debug("Input: " + str(case.input))
        result = nlp.restructure(case.input, case.html_meta)
        log.debug("Result: " + str(result))
        assert(result == case.expected_output)

##########################################
##########################################
# Test nlp pipeline
##########################################
##########################################


class TestNlpPipeline():
    class NlpPipelineTestCase():
        def __init__(self,
                     name,
                     input,
                     expected_output,
                     html_meta=False,
                     remove_stopwords=False,
                     lemmatize=False):
            self.name = name
            self.input = input
            self.html_meta = html_meta
            self.remove_stopwords = remove_stopwords
            self.lemmatize = lemmatize
            self.expected_output = expected_output

    to_run_through_nlp_pipeline = [
        NlpPipelineTestCase(
            name="Nominal",
            input="Clear sentence needs some processing",
            html_meta=False,
            remove_stopwords=False,
            lemmatize=False,
            expected_output=["Clear", "sentence",
                             "needs", "some", "processing"]
        ),
        NlpPipelineTestCase(
            name="Stopword",
            input="This sentence needs some processing",
            html_meta=False,
            remove_stopwords=True,
            lemmatize=False,
            expected_output=["sentence", "needs", "processing"]
        ),
        NlpPipelineTestCase(
            name="Nominal html meta",
            input="whyIsThisAllGlued",
            html_meta=True,
            remove_stopwords=True,
            lemmatize=True,
            expected_output=["glue"]
        ),
        NlpPipelineTestCase(
            name="Long sentence",
            input="spaCy determines the part-of-speech tag by default and assigns the corresponding lemma.",
            html_meta=False,
            remove_stopwords=True,
            lemmatize=True,
            expected_output=["spaCy", "determines", "part", "speech",
                             "tag", "default", "assign", "correspond", "lemma", "."]
        ),
        NlpPipelineTestCase(
            name="Oscar Wilde quote (remove stopwords, lemmatize)",
            input="Be yourself; everyone else is already taken.",
            html_meta=False,
            remove_stopwords=True,
            lemmatize=True,
            expected_output=["everyone", "else", "already", "take", "."]
        ),
        NlpPipelineTestCase(
            name="Oscar Wilde quote (remove stopwords)",
            input="Be yourself; everyone else is already taken.",
            html_meta=False,
            remove_stopwords=True,
            lemmatize=False,
            expected_output=["everyone", "else", "already", "taken", "."]
        ),
        NlpPipelineTestCase(
            name="Oscar Wilde quote (leave stopwords, don't lemmatize)",
            input="Be yourself; everyone else is already taken.",
            html_meta=False,
            remove_stopwords=False,
            lemmatize=False,
            expected_output=["Be", "yourself", "everyone",
                             "else", "is", "already", "taken", "."]
        ),
        NlpPipelineTestCase(
            name="Dollar amount)",
            input="42$",
            html_meta=False,
            remove_stopwords=False,
            lemmatize=False,
            expected_output=["42$"]
        ),
        NlpPipelineTestCase(
            name="Dollar amount)",
            input="$42",
            html_meta=False,
            remove_stopwords=False,
            lemmatize=False,
            expected_output=["$42"]
        )
    ]

    @pytest.mark.parametrize("case", to_run_through_nlp_pipeline)
    def test_nlp_preprocessing_pipeline(self, case):
        log.info("Case: " + case.name)
        log.debug("Input: " + str(case.input))
        result = nlp.preprocessing_pipeline(
            sentence=case.input,
            html_meta=case.html_meta,
            remove_stopwords=case.remove_stopwords,
            lemmatize=case.lemmatize)
        log.debug("Result: " + str(result))
        assert(result == case.expected_output)
