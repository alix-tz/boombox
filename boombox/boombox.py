# boombox - A simple noise generator for XML ALTO data
# Author: Alix Chagué
# Date: 2023-03-13
# License: MIT
# Version: 0.1.0
# Path: boombox\boombox.py

import random
import textdistance
import typo
import unicodedata

import lxml.etree as ET

# import utils
from .utils import *


# = = = = = = = = = = Add random noise


def blank_or_x(word_replacement_opts) -> str:
    """Return a blank string or a string of Xs, or other characters if specified in config.py"""
    # imitates when a transcriber doesn't understand a word and leaves it blank or replaces it with Xs)
    word_replacement_opts = check_and_fix_weights(word_replacement_opts)
    replacement = random.choices(
        population=list(word_replacement_opts.keys()),
        weights=list(word_replacement_opts.values()),
        k=1,
    )[0]
    return replacement * random.randint(2, 5)


# = = = = = = = = = = Main class definition
class BoomBox:
    name = "BoomBox"

    def __init__(self, path, file_type, seed=None):
        self.path = path
        self.file_type = file_type
        self.seed = seed
        self.stats = {}
        self.original = None
        self.noisy = None

    def _replace_word(
        self, string, word_replacement_opts, word_replacement_prob
    ) -> str:
        """Replace a random word with a blank string or a string of Xs, or other characters if specified in config.py"""
        # imitates when a transcriber doesn't understand a word and leaves it blank or replaces it with Xs)
        words = string.split(" ")
        hit = 0
        for i, word in enumerate(words):
            if random.random() < word_replacement_prob:
                hit += 1
                words[i] = blank_or_x(word_replacement_opts)
        if hit > 0:
            self.stats["replaced_words"] += hit
        return " ".join(words), hit

    def _random_typo(self, string, typo_opts: dict, typo_prob: float) -> str:
        """Apply random typos to a string, according to the specified modes and weights"""
        myStrErrer = typo.StrErrer(string, seed=self.seed)
        typo_opts = pop_invalid_modes(typo_opts)
        typo_opts = check_and_fix_weights(typo_opts)
        hit = 0
        for i in range(0, len(string)):
            if random.random() < typo_prob:
                hit += 1
                mode = random.choices(
                    population=list(typo_opts.keys()),
                    weights=list(typo_opts.values()),
                    k=1,
                )[0]
                if mode == "swap":
                    myStrErrer.char_swap()
                elif mode == "delete":
                    myStrErrer.missing_char()
                elif mode == "insert":
                    myStrErrer.extra_char()
                elif mode == "nearby":
                    myStrErrer.nearby_char()
                elif mode == "similar":
                    myStrErrer.similar_char()
                elif mode == "agglomerate":
                    myStrErrer.skipped_space()
                elif mode == "split":
                    myStrErrer.random_space()
                elif mode == "repeat":
                    myStrErrer.repeated_char()
                elif mode == "unichar":
                    myStrErrer.unichar()
        if hit > 0:
            self.stats["affected_chars"] += hit
            self.stats["affected_lines"] += 1
        return myStrErrer.result, hit

    def _compile_stats(self):
        """Compile statistics about the noise generation"""
        self.stats["original"] = "\n".join(self.original)
        self.stats["noisy"] = "\n".join(self.noisy)
        self.stats["original_nchars"] = len(self.stats["original"].replace("\n", ""))
        self.stats["noisy_nchars"] = len(self.stats["noisy"].replace("\n", ""))
        self.stats["original_nlines"] = len(self.original)
        self.stats["noisy_nlines"] = len(self.noisy)
        self.stats["nchars_diff"] = (
            self.stats["noisy_nchars"] - self.stats["original_nchars"]
        )
        self.stats["nlines_diff"] = (
            self.stats["noisy_nlines"] - self.stats["original_nlines"]
        )
        self.stats["Levenshtein"] = textdistance.levenshtein.distance(
            self.stats["original"], self.stats["noisy"]
        )
        self.stats["CER"] = self.stats["Levenshtein"] / self.stats["original_nchars"]

    def _add_noise_alto(self, noise_opts, save=True, path_out=None):
        """Add noise to an XML ALTO file"""
        xml = load_alto_xml(self.path)
        lines = get_strings_in_alto(xml)

        self.stats["affected_lines"] = 0
        self.stats["affected_chars"] = 0
        self.stats["replaced_words"] = 0

        self.original = []
        self.noisy = []

        for line in lines:
            string = unicodedata.normalize("NFC", line.get("CONTENT", "")).strip()
            if string:
                self.original.append(string)
                # applying typo
                noisy_string, hit_char = self._random_typo(
                    string, noise_opts["typo_opts"], noise_opts["typo_prob"]
                )
                # applying word replacement
                noisy_string, hit_word = self._replace_word(
                    noisy_string,
                    noise_opts["word_replacement_opts"],
                    noise_opts["word_replacement_prob"],
                )
                if hit_char == 0 and hit_word > 0:
                    self.stats["affected_lines"] += 1
                self.noisy.append(noisy_string)
                line.set("CONTENT", noisy_string)

        if save is True:
            if not path_out:
                path_out = self.path.replace(".xml", "_noisy.xml")
            save_noisy_alto_xml(path_out, xml)

        self._compile_stats()

    def _add_noise_text(self, noise_opts, save=True, path_out=None):
        # Todo: generated with copilot, make sure it does what it's supposed to do
        """Add noise to a text file"""
        with open(self.path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        self.stats["affected_lines"] = 0
        self.stats["affected_chars"] = 0
        self.stats["replaced_words"] = 0

        self.original = []
        self.noisy = []

        for line in lines:
            string = unicodedata.normalize("NFC", line).strip()
            if string:
                self.original.append(string)
                # applying typo
                noisy_string, hit_char = self._random_typo(
                    string, seed=self.seed, **noise_opts
                )
                # applying word replacement
                noisy_string, hit_word = self._replace_word(noisy_string, **noise_opts)
                if hit_char == 0 and hit_word > 0:
                    self.stats["affected_lines"] += 1
                self.noisy.append(noisy_string)

        if save is True:
            if not path_out:
                path_out = self.path.replace(".txt", "_noisy.txt")
            save_noisy_text(path_out, "\n".join(self.noisy))

        self._compile_stats()

    def add_noise(self, noise_opts=None, save=True, path_out=None):
        if noise_opts is None:
            noise_opts = {}
        if self.file_type == "alto":
            if is_alto(self.path) is False:
                print(f"{self.path} is not an ALTO file")
            else:
                self._add_noise_alto(noise_opts, save=save, path_out=path_out)
        elif self.file_type == "text":
            self._add_noise_text(noise_opts, save=save, path_out=path_out)
        else:
            raise ValueError("File type not supported")

    def get_stats(self):
        return self.stats

    def get_cer(self):
        return self.stats.get("CER", "No CER available")



