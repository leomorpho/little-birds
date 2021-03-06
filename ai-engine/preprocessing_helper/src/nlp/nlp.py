import nltk
import spacy
import re
import sys
import logging
import config
import string
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import words
import enchant
from .constants_en import CONTRACTION_MAP, META_WORDS_OF_INTEREST, USELESS_HTML_ATTRS_CONSTANTS
from typing import Set, List, Optional, Any

NLTK_DICT = set(words.words())
log = logging.getLogger()
log.setLevel(config.LOG_LEVEL)


stopword_list = nltk.corpus.stopwords.words('english')
stopword_list.remove('no')
stopword_list.remove('not')
stopword_list.remove('to')
#tokenizer = ToktokTokenizer()
spacy_nlp = spacy.load('en_core_web_sm', parse=True, tag=True, entity=True)
dictionnary = enchant.Dict()


# def important_words(data: str) -> set():
#     # Extract only words with letters
#     if not data.isalpha():
#         return

#     # Split words of the form: 'forSalePrice', 'VehicleList'
#     restructure: Set[str] = set(re.sub( r"([A-Z])", r" \1", data).split())
#     data = map(lambda x: x.lower(), restructure)

#     data = set(filter(lambda x: len(x) > 2, data))
#     data = data - set(stopword_list)
#     data = data - USELESS_HTML_ATTRS_CONSTANTS

#     data = set(map(lambda x: lemmatize_text(x), data))
#     data = data & NLTK_DICT

#     return data

def preprocessing_pipeline(sentence: str,
                           html_meta: bool = False,
                           remove_stopwords=False,
                           lemmatize=True
                           ) -> str:
    """A full NLP pipeline to run on a string
    :param sentence: the sentence to be processed
    :type  sentence: str
    :param do_restructure: split words of the form splitWords to 'split words'
    :type  do_restructure: bool
    :param sequence: whether the supplied sentence must be treated as a sequence or a set
    :type  sequence: bool
    """
    # NOTE: do not add space between kept punctuation and its neighbours,
    # for example $54, not $ 54

    # (1) Run processes that change the length of the sentence
    # TODO: Not efficient, but let's fix that later...
    # Split and remove words (concatenations, contractions, stop words...)
    sentence: str = restructure(sentence, html_meta=html_meta)

    if sentence and remove_stopwords:
        sentence = remove_stopwords_from_list(sentence)

    if sentence and lemmatize:
        sentence = [lemmatize_text(word) for word in sentence]

    if sentence and html_meta:
        # Remove words not in dictionnary
        sentence = [word for word in sentence if (dictionnary.check(
            word) and word not in USELESS_HTML_ATTRS_CONSTANTS)]
    return sentence


def restructure(sentence: str, html_meta: bool = False) -> List[str]:
    """Split contracted words and elimites unwanted ones
    :param word: a word that may need splitting
    :type  word: str
    :param html_meta: determines if html classes and the like have to be
    parsed to yield useful data. Not needed for regular text.
    Example: "<cite class="somethingThatNeedsToBeSplit"></cite>"
    """
    sentence: List[str] = sentence.split()

    # Can't change the length of a list while iterating over it, so create a new one.
    parsed_sentence: List[str] = []

    # TODO: Lots of loops here, it's inneficient, but it will do for now...
    for word in sentence:
        restructured: List[str] = []
        # If the word is NOT an html tag
        if word[0] != "<" and word[-1] != ">":
            # (1) Split if required
            if html_meta:
                # Replace non-alpha chars
                word = re.sub(r"[^a-zA-Z]+", ' ', word)
                # Add space before capitals
                word = re.sub(r"(?<=\w)([A-Z])", r" \1", word)
                word = word.lower()
                restructured = word.split()

                # Remove all one letter words
                restructured = [word for word in restructured if len(word) > 2]

            else:
                # Add space before punctuation
                word = re.sub(r'([.,!?()-])', r' \1', word)
                # (2) Expand contracted words
                restructured = expand_contractions_in_list(word.split())
                # (3) Remove unwanted chars
                restructured = remove_chars_from_list(restructured,
                                                      acceptable_chars_list=[",", ".", ":", "$", "%", "?", "'"])
                # restructured = list(map(lambda x: x.strip(), restructured))
        else:
            # An html tag
            restructured.append(word)
        # Append restructured word to new sentence
        parsed_sentence = parsed_sentence + restructured
    return parsed_sentence


def remove_chars_from_list(sentence: List[str],
                           acceptable_chars_list: Optional[list] = None,
                           alpha_only=False) -> List[str]:
    """Removes all characters except for the ones in the acceptable list.
    It is expected that the elements of the supplied list are individual "words" and not
    whole strings of words.
    Example: ["This", "is", "a", "sentence"] is valid
    whereas  ["This is a sentence"] is invalid
    :param alpha_only: Remove all non-letters
    :type  alpha_only: bool
    """
    parsed_sentence: List[str] = []

    # String to store unwanted chars
    unwanted: str = string.punctuation + '“'

    # TODO: current list of unwanted chars do not comprise ASCII chars. It remains
    # very limited for now and should be expanded.
    for word in sentence:
        if alpha_only:
            word = re.sub(r"[^a-zA-Z]+", '', word)
        elif word[0] != "<" and word[-1] != ">":
            if acceptable_chars_list:
                unwanted = ''.join(set(unwanted) - set(acceptable_chars_list))
            word = word.translate(str.maketrans('', '', unwanted))
        if word:
            parsed_sentence.append(word)
    return parsed_sentence


def expand_contractions_in_list(words: List[str]) -> List[str]:
    expanded_words: List[str] = []
    for word in words:
        expanded_words.extend(expand_contraction(word).split())
    return expanded_words


def expand_contraction(word: str, contraction_mapping: dict = CONTRACTION_MAP) -> str:
    try:
        expanded = contraction_mapping[word]
        return expanded
    except:
        return word


def remove_stopwords_from_list(word_list: List[str], is_lower_case=False) -> List[str]:
    if is_lower_case:
        word_list = list(filter(lambda x: x not in stopword_list, word_list))
        # [w for w in word_list if w not in stopword_list]
    else:
        #filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
        word_list = list(
            filter(lambda x: x.lower() not in stopword_list, word_list))
    return word_list


def lemmatize_text(text: str) -> str:
    # Do not lemmatize numbers or prices
    text = spacy_nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ !=
                     '-PRON-' else word.text for word in text])
    return text
