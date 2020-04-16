import os
import csv
import logging 
import typing
import config

log = logging.getLogger()
log.setLevel(config.LOG_LEVEL)

class MetaWordsImprover():
    def __init__(self, metawords_filepath):
        self.filename_metawords = metawords_filepath
        if os.path.exists(self.filename_metawords) is False:
            log.info("creating csv file")
            with open(self.filename_metawords, "w") as f:
                writer = csv.writer(f)
                writer.writerow(["id", "count", "word"])
  
    def update_list(self, set_of_words: set()) -> None:
        for word in set_of_words:
            self._update_or_add_word(word, self.filename_metawords)
                
    def _update_or_add_word(self, word_to_update_or_add: str, file: typing.TextIO) -> None:
        lines = []
        with open(self.filename_metawords, "r") as file:
            reader = csv.reader(file)
            lines = list(reader)
            word_updated = False
            for line in lines:
                if line[2] == word_to_update_or_add:
                    count = line[1]
                    count = str(int(count) + 1)
                    line[1] = count
                    word_updated = True
            if word_updated is False:
                lines.append(["id", 1, word_to_update_or_add])
        
        with open(self.filename_metawords, "w") as file:
            writer = csv.writer(file)
            writer.writerows(lines)
        