# !/usr/bin/env python
# -*- coding: utf-8 -*-
from get_metadata import Article
from get_analysis import Text, update
from pathlib import Path, PurePosixPath
import json


class CorpusItemBuilder:
    _article_id = 0

    def __init__(self, text: str, folder_counter):
        self.text = text
        self.journal_type = folder_counter
        CorpusItemBuilder._article_id += 1

        self.metadata = {"journal": "",
                         "journal type": "",
                         "author": [],
                         "institution": "",
                         "title": [],
                         "doi": "",
                         "year": "",
                         "udc": "",
                         "keywords": {"in Ukrainian": [], "in English": [], "in russian": []},
                         "annotation": {"in Ukrainian": "", "in English": "", "in russian": ""},
                         "abbreviations": {"in Ukrainian": [], "in English": []},
                         "sources": {"in Ukrainian": [], "in English": []},
                         "references": {"in Ukrainian": [], "in English": []}}
        self.text_structure = {"number of words": 0,
                               "number of sentences": 0,
                               "number of paragraphs": 0,
                               "number of drawings": 0,
                               "number of tables": 0,
                               "number of diagrams": 0,
                               "number of graphs": 0,
                               "number of lists": 0,
                               "number of examples": 0,
                               "average word length": 0,
                               "median word length": 0,
                               "average sentence length in words": 0,
                               "median sentence length in words": 0,
                               "average paragraph length in sentences": 0,
                               "median paragraph length in sentences": 0,
                               "number of subordinate clauses": 0,
                               "average number of subordinate clauses per sentence": 0,
                               "median number of subordinate clauses per sentence": 0,
                               "dictionary of subordinates": {},
                               "number of functors": 0,
                               "average number of functors per sentence": 0,
                               "median number of functors per sentence": 0,
                               "dictionary of functors": {},
                               "number of -nnia nouns": 0,
                               "average number of -nnia nouns": 0,
                               "median number of -nnia nouns per sentence": 0,
                               "dictionary of -nnia nouns": {},
                               "number of -sia verbs": 0,
                               "dictionary of -sia verbs": {},
                               "average number of -sia verbs per sentence": 0,
                               "median number of -sia verbs per sentence": {},
                               "number of -no, -to verbs": 0,
                               "dictionary of -no, -to verbs": {},
                               "average number of -no, -to verbs per sentence": 0,
                               "median number of -no, -to verbs per sentence": 0,
                               "number of modal words": 0,
                               "dictionary of modal words": {},
                               "average number of modal words per sentence": 0,
                               "median number of modal words per sentence": 0,
                               "number of first pronouns": 0,
                               "dictionary of first pronouns": {},
                               "average number of first pronouns per sentence": 0,
                               "median number of first pronouns per sentence": 0,
                               "number of cited words": 0,
                               "number of peoples' mentions": 0,
                               "list of peoples' mentions": [],
                               "number of punctuation marks": 0,
                               "average number of punctuation marks per sentence": 0,
                               "dictionary of punctuation marks": {},
                               "text": ""}
        self.structure_per_paragraph = {}
        self.text_and_statistics = {"id": CorpusItemBuilder._article_id,
                                    "type": "article",
                                    "metadata": self.metadata,
                                    "whole text": self.text,
                                    "text structure": self.text_structure,
                                    "structure per paragraph": self.structure_per_paragraph}

    def build_item(self):
        article = Article(self.text, self.metadata, self.journal_type)
        print("ARTICLE CREATED")
        self.text, self.metadata = article.parse_it()
        print("METADATA FETCHED")
        article = Text(self.text, self.text_structure, self.structure_per_paragraph)
        print("ARTICLE 2 CREATED")
        self.text_structure, self.structure_per_paragraph = article.parse_it()
        print("ANALYSIS FETCHED")

        # print(json.dumps(self.metadata, indent=4, ensure_ascii=False))
        # print(json.dumps(self.text_structure, indent=4, ensure_ascii=False))

        return self.text_and_statistics


def iterate(folder) -> list:
    folder = Path(folder)
    paths = []
    for element in folder.iterdir():
        if element.is_dir():
            paths.extend(iterate(element))
        if element.is_file() and PurePosixPath(str(element)).suffix == '.txt':
            paths.append(str(element))
    return paths


def calculate(subcorpora):
    statistics = {}
    general_dictionary_of_subordinates = {}
    general_dictionary_of_functors = {}
    general_dictionary_of_nnia_nouns = {}
    general_dict_of_sia_verbs = {}
    general_dict_of_no_to_verbs = {}
    general_dict_of_modal_words = {}
    general_dict_of_first_pronouns = {}
    general_dictionary_of_punctuation_marks = {}

    for subcorpus in subcorpora.keys():
        for corpus_item in subcorpora[subcorpus].keys():
            text_statistics = subcorpora[subcorpus][corpus_item]["text structure"]
            if "text" in text_statistics.keys():
                text_statistics.pop("text")

            for parameter in text_statistics.keys():
                if subcorpus not in statistics.keys():
                    statistics[subcorpus] = {}
                if parameter not in statistics[subcorpus].keys():
                    statistics[subcorpus][parameter] = []
                statistics[subcorpus][parameter].append(text_statistics[parameter])

            for parameter in statistics[subcorpus].keys():
                try:
                    if type(statistics[subcorpus][parameter]) == list:
                        statistics[subcorpus][parameter].sort()
                except TypeError:
                    pass

            statistics[subcorpus]["general dictionary of subordinates"] = update(
                general_dictionary_of_subordinates, text_statistics["dictionary of subordinates"])
            statistics[subcorpus]["general dictionary of functors"] = update(
                general_dictionary_of_functors, text_statistics["dictionary of functors"])
            statistics[subcorpus]["general dictionary of -nnia nouns"] = update(
                general_dictionary_of_nnia_nouns, text_statistics["dictionary of -nnia nouns"])
            statistics[subcorpus]["general dictionary of -sia verbs"] = update(
                general_dict_of_sia_verbs, text_statistics["dictionary of -sia verbs"])
            statistics[subcorpus]["general dictionary of -no, -to verbs"] = update(
                general_dict_of_no_to_verbs, text_statistics["dictionary of -no, -to verbs"])
            statistics[subcorpus]["general dictionary of modal words"] = update(
                general_dict_of_modal_words, text_statistics["dictionary of modal words"])
            statistics[subcorpus]["general dictionary of first pronouns"] = update(
                general_dict_of_first_pronouns, text_statistics["dictionary of first pronouns"])
            statistics[subcorpus]["general dictionary of punctuation marks"] = update(
                general_dictionary_of_punctuation_marks, text_statistics["dictionary of punctuation marks"])
    return statistics


def build_the_corpus():
    folder_test_empty = "C:\\Users\\Bohdanka\\PycharmProjects\\Навчання\\2 курс\\Курсова\\Корпус наукових статей\\test_empty"
    paths = [iterate(folder_test_empty)]

    # folder = "D:\\НАВЧАННЯ\\2 курс\\КУРСОВА\\Корпус"
    # folder_scientific = "C:\\Users\\Bohdanka\\PycharmProjects\\Навчання\\2 курс\\Курсова\\Корпус наукових статей\\Corpus\\Good articles"
    # scientific_paths = iterate(folder_scientific)
    # folder_predatory = "C:\\Users\\Bohdanka\\PycharmProjects\\Навчання\\2 курс\\Курсова\\Корпус наукових статей\\Corpus\\Bad articles"
    # predatory_paths = iterate(folder_predatory)
    # paths = (predatory_paths, scientific_paths)
    corpus = {}
    subcorpora = {}

    def dict_key(dic: dict, key) -> dict:
        if key not in dic.keys():
            dic[key] = {}
        return dic[key]

    def get_counter(dic: dict):
        if dic:
            return str(max([int(key) for key in dic.keys()]) + 1)
        return "1"

    for counter in range(len(paths)):
        for path in paths[counter]:
            print(path)
            with open(path, 'r', encoding='utf-8') as file:
                text = file.read()
            article = CorpusItemBuilder(text, counter)
            corpus_entity = article.build_item()
            corpus[str(CorpusItemBuilder._article_id)] = corpus_entity

            journal_type = corpus_entity["metadata"]["journal type"]
            if journal_type == "predatory" or journal_type == "scientific":
                dict_key(subcorpora, journal_type)[get_counter(subcorpora[journal_type])] = corpus_entity
            else:
                print("{}{:^20}\n{}".format("NO JOURNAL TYPE", journal_type, corpus_entity))

            journal = corpus_entity["metadata"]["journal"]
            if "лінгвістичні студії" in journal.lower():
                dict_key(subcorpora, "ling_stud")[get_counter(subcorpora["ling_stud"])] = corpus_entity
            elif "українське мовознавство" in journal.lower():
                dict_key(subcorpora, "ukr_mov")[get_counter(subcorpora["ukr_mov"])] = corpus_entity
            elif "логос" in journal.lower():
                dict_key(subcorpora, "logos")[get_counter(subcorpora["logos"])] = corpus_entity
            elif "молодий вчений" in journal.lower():
                dict_key(subcorpora, "young_sci")[get_counter(subcorpora["young_sci"])] = corpus_entity
            elif "наука" in journal.lower():
                dict_key(subcorpora, "science")[get_counter(subcorpora["science"])] = corpus_entity
            else:
                print("{}{:^20}\n{}".format("JOURNAL DOESN'T FIT", journal, corpus_entity))
            print("ONE DONE")

    statistics = calculate(subcorpora)

    def check_name(corpus_name, counter=0, ending='.json'):
        corpus_path = Path(corpus_name+str(counter)+ending)
        if corpus_path.exists():
            return check_name(corpus_name, counter=counter+1, ending='.json')
        return corpus_name+str(counter)+ending

    with open(check_name('Corpus_of_Science_Articles_'), 'w', encoding='utf-8') as file:
        json.dump(corpus, file, indent=4, ensure_ascii=False)

    with open(check_name('Subcorpora_of_Science_Articles_'), 'w', encoding='utf-8') as file:
        json.dump(subcorpora, file, indent=4, ensure_ascii=False)

    with open(check_name('Statistics_of_Science_Articles_'), 'w', encoding='utf-8') as file:
        json.dump(statistics, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    build_the_corpus()
    print("FINISH")

    # test = "C:\\Users\\Bohdanka\\PycharmProjects\\Навчання\\2 курс\\Курсова\\Корпус наукових статей\\Corpus\\Good articles\\Лінгвістичні студії ДоНУ\\2021\\Громко - Граматична система говірки за даними дескрипції. Іменникові форми.txt"
    # with open(test, 'r', encoding='utf-8') as file:
    #     # print(json.dumps(text, indent=4, ensure_ascii=False))
    #     text = file.read()
    #     article = CorpusItemBuilder(text, True)
    #     analyzed = article.build_item()
    #     # print(analyzed)
    #     print(json.dumps(analyzed, indent=4, ensure_ascii=False))
