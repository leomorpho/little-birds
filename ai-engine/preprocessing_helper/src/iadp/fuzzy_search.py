from fuzzywuzzy import process
from typing import List

def process_search_term(search_term: str) -> List[str]:
    choices = ["job posting", "classified", "newspaper article", "newspaper"]
    return process.extract(search_term, choices, limit=3)