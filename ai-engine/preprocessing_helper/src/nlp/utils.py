import nltk
import spacy
import re
import sys
import logging
import config
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import words
from .constants_en import CONTRACTION_MAP, META_WORDS_OF_INTEREST, USELESS_HTML_ATTRS_CONSTANTS
from typing import Set, List

NLTK_DICT = set(words.words())
log = logging.getLogger()
log.setLevel(config.LOG_LEVEL)


stopword_list = nltk.corpus.stopwords.words('english')
stopword_list.remove('no')
stopword_list.remove('not')
stopword_list.remove('to')
tokenizer = ToktokTokenizer()
nlp = spacy.load('en_core_web_sm', parse=True, tag=True, entity=True)

def expand_contractions(text: str, contraction_mapping=CONTRACTION_MAP) -> str: 
    contractions_pattern = re.compile('({})'.format(
        '|'.join(contraction_mapping.keys())), flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())                       
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
        
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text

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

def important_words(data: str) -> set():
    # Extract only words with letters
    if not data.isalpha():
        return

    # Split words of the form: 'forSalePrice', 'VehicleList'
    split_words: Set[str] = set(re.sub( r"([A-Z])", r" \1", data).split())
    data = map(lambda x: x.lower(), split_words)

    data = set(filter(lambda x: len(x) > 2, data))
    data = data - set(stopword_list)
    data = data - USELESS_HTML_ATTRS_CONSTANTS
        
    data = set(map(lambda x: lemmatize_text(x), data))
    data = data & NLTK_DICT

    return data

def nlp_pipeline(sentence:List[str], 
                 split_words:bool=False, 
                 sequence:bool=True
                 ) -> str:
    """A full NLP pipeline to run on a string
    :param sentence: the sentence to be processed
    :type  sentence: str
    :param split_words: split words of the form splitWords to 'split words'
    :type  split_words: bool
    :param sequence: whether the supplied sentence must be treated as a sequence or a set
    :type  sequence: bool
    """
    # NOTE: do not add space between kept punctuation and its neighbours, 
    # for example $54, not $ 54
        
    if split_words:
        sentence = split_words(sentence)
    
    # for word in sentence:
    #     pass
        
    #     # Remove punctuation
    #     # Remove stopwords
    #     # Expand contractions
        
    #     # Lemmatize
    #     # Verify word is in dictionnary if not number or other symbol
    
    return sentence

def split_words(sentence: List[str]) -> List[str]:
    """Splits words of the form helloThere, WhatIsUp to 'hello there' and 'what is up'
    :param word: a word that may need splitting
    :type  word: str
    """
    new_sentence: List[str] = []
    for word in sentence:
        split_words = list(re.sub( r"([A-Z])|(_)", r" \1", word).split())
        if len(split_words) > 1:
            new_sentence.extend(split_words)
        else:
            new_sentence.append(word)
    return new_sentence