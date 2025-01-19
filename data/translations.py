import json
import os

current_dir = os.path.dirname(__file__)


class Translator:
    def __init__(self, trns_file: str = os.path.join(current_dir, "translation.json") ):
        with open(trns_file, "r", encoding="utf-8") as file:
            self.trns_file = json.load(file)

    def trns(self, text, lang="ru"):
        if lang == "ru":
            return text
        else:
            try:
                return self.trns_file[lang][text]
            except KeyError:
                return text
            