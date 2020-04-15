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
from typing import Set, List, Optional

NLTK_DICT = set(words.words())
log = logging.getLogger()
log.setLevel(config.LOG_LEVEL)


stopword_list = nltk.corpus.stopwords.words('english')
stopword_list.remove('no')
stopword_list.remove('not')
stopword_list.remove('to')
tokenizer = ToktokTokenizer()
nlp = spacy.load('en_core_web_sm', parse=True, tag=True, entity=True)
dictionnary = enchant.Dict()

def remove_stopwords(text: str, is_lower_case=False) -> str:
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)    
    return filtered_text

def lemmatize_text(text: str) -> str:
    # Do not lemmatize numbers or prices
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text

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

def nlp_pipeline(sentence:List[str], 
                 do_split:bool=False, 
                 sequence:bool=True
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
    sentence = restructure(sentence, do_split)
    
    # # (2) Run processes that run in-place in the list (and do not change its length)
    # for key, word in enumerate(sentence):
    #     # strip spaces
    #     sentence[key] = word.strip()
    #     # Remove stopwords
    #     if word in stopword_list:
    #         sentence[key] = ""
    #     # Lemmatize
    #     # Verify word is in dictionnary if not number or other symbol
    #     if dictionnary.check(word) is False:
    #         sentence[key] = ""
        # Remove empty html elements
    
    # # Remove all empty elements
    sentence = [word for word in sentence if " " not in word]
    # log.info("nlp_pipeline: " + str(sentence))
    
    return sentence

def add_to_list(mylist: List[str], elem: List[str]):
    if len(mylist) is None or elem is None:
        raise ValueError("List and/or element must not be None")
    if len(elem) == 0:
        return mylist
    if len(elem) == 1:
        return mylist.append(elem[0])
    else:
        return mylist.extend(elem)
    

def restructure(sentence:List[str], do_split:bool=False) -> List[str]:
    """Split contracted words and elimites unwanted ones
    :param word: a word that may need splitting
    :type  word: str
    """
    new_sentence: List[str] = []
    
    for word in sentence:
        restructure: List[str] = []
        if word[0] != "<" and word[-1] != ">":
            # (1) Split if required
            if do_split:
                split_word = split_word(word)
                restructure = add_to_list(restructure, split_word)
            restructure = add_to_list(restructure, word)
            # (2) Expand contracted words
            # restructure = map(lambda x: expand_contractions(x), restructure)
            
            # (3) Remove unwanted chars
            # (4) Remove stopwords
        else:
            # An html tag
            restructure = []
        log.error("type(restructure): " + type(restructure))
        if len(restructure) > 1:
            new_sentence.extend(restructure)
        else:
            new_sentence.append(restructure[0])
    return new_sentence

def split_word(word:str, pattern:str=None):
    """Splits words at the given pattern.
    This function is not aware of html tags, and if one is supplied in the word,
    it will be treated like a regular word.
    Example: "<ArtiCle>" will become ["<Arti", "Cle>"]
    """
    result =  list(re.sub( r"([A-Z])|(_)", r" \1", word).split())
    log.info("RESULT HERE ***********************")
    return result
    
def remove_chars_from_word(sentence:List[str], 
                               acceptable_chars_list:Optional[list]=None) -> List[str]:
    """Removes all characters except for the ones in the acceptable list.
    It is expected that the elements of the supplied list are individual "words" and not 
    whole strings of words.
    Example: ["This", "is", "a", "sentence"] is valid
    whereas  ["This is a sentence"] is invalid
    """
    # TODO: current list of unwanted chars do not comprise ASCII chars. It remains 
    # very limited for now and should be expanded.
    unwanted: str = string.punctuation + '“'
    if acceptable_chars_list:
        unwanted = ''.join(set(unwanted) - set(acceptable_chars_list))
   
    new_sentence: List[str] = []
    for word in sentence:
        if word[0] != "<" and word[-1] != ">":
            word = word.translate(str.maketrans('', '', unwanted))
        if word:
            new_sentence.append(word)
    return new_sentence


def expand_contractions(word:str, contraction_mapping:dict=CONTRACTION_MAP) -> List[str]: 
    try:
        expanded = contraction_mapping[word]
        return expanded
    except:
        return word