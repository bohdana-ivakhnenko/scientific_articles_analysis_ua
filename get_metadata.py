# !/usr/bin/env python
# -*- coding: utf-8 -*-
import re


class Article:
    type = 'article'

    def __init__(self, whole_text: str,  metadata: dict, folder_counter):
        self.text = whole_text
        self.metadata = metadata
        self.folder_counter = folder_counter

        self.list_of_authors = []
        self.name_of_institution = ""
        self.article_title = []
        self.year_of_publication = 0
        self.journal = ""
        self.article_udc = ""
        self.article_doi = ""

        self.list_of_keywords_ukrainian = []
        self.list_of_keywords_english = []
        self.list_of_keywords_russian = []

        self.annotation_ukrainian = ""
        self.annotation_english = ""
        self.annotation_russian = ""

        self.abbreviations_ukrainian = ""
        self.abbreviations_english = ""

        # література
        self.list_of_references_ukrainian = []
        self.list_of_references_english = []
        # self.list_of_references_russian = []

        # джерела, матеріяли
        self.list_of_sources_ukrainian = []
        self.list_of_sources_english = []
        # self.list_of_sources_russian = []

    @staticmethod
    def get_it(pattern, text, list_output=False, replace=False, integer=False):
        parameter_to_fill = []
        if type(text) == list:
            [parameter_to_fill.extend(pattern.findall(passage)) for passage in text if pattern.findall(passage)]
            if replace:
                text = [pattern.sub("", passage) for passage in text]
        elif type(text) == str:
            # print(pattern.findall(text))
            parameter_to_fill.extend(pattern.findall(text))
            if replace:
                text = pattern.sub("", text)
        if integer and parameter_to_fill:
            return int(parameter_to_fill[0]), text
        if list_output:
            return [re.sub("[\n\t]", " ", p).strip() for p in parameter_to_fill], text
        if len(parameter_to_fill) == 1:
            return re.sub(r"\n", " ", parameter_to_fill[0]).strip("\t "), text
        return re.sub("\n", " ", ' '.join(parameter_to_fill)).strip("\t "), text

    def get_keywords(self) -> tuple:
        keywords_ukrainian_pattern \
            = re.compile(r"""(?x)(?<=[KКк]люч[оoеe]в[іi]\s[сc]л[оo]в[аa])(?:[^.]+?[,;]?)+""")
        keywords_english_pattern \
            = re.compile(r"""(?x)(?:(?<=[Kk]eywords)|(?<=[Kk]ey\swords))[^ ]
            (?:[-−–\w\s’'“”/\"«»()]+(?:[,;]\n?\ ?)?)+(?=\.?)""")
        keywords_russian_pattern \
            = re.compile(r"""(?x)(?<=[Кк]люч[оoеe]вы[еe]\ [сc]л[оo]в[аa])[^ ]
            (?:[-−–А-ЯІЇЄҐа-яіїєґ\w ’'“”/\"«»()]+(?:[,;]\n?\ ?)?)+(?=\.?)""")
        keywords_ukrainian, self.text = self.get_it(keywords_ukrainian_pattern, self.text, replace=True)
        keywords_english, self.text = self.get_it(keywords_english_pattern, self.text, replace=True)
        keywords_russian, self.text = self.get_it(keywords_russian_pattern, self.text, replace=True)
        return re.split('[,;] ', keywords_ukrainian.strip(" :-–-")), \
            re.split('[,;] ', keywords_english.strip(" :-–-")), re.split('[,;] ', keywords_russian.strip(" :-–-"))

    def get_journal(self, part_of_text) -> tuple:
        journal_pattern = re.compile(r"«?[А-ЯҐЇЄІ][а-яґіїє].+?»?(?=,|\.? [№•]|[А-ЯҐЇЄІ]{4,}|\n|$)")
        return self.get_it(journal_pattern, part_of_text, replace=True)

    def get_authors_name(self, part_of_text) -> tuple:
        name_pattern = re.compile(r"""(?x)
(?<!.{5}[“\d]|.{2}ім\.\s|імені\s)
(?:
(?:[А-ЯҐЇЄІ][а-яґіїє'`ʼ]?\s*?\.\s*?(?:[-−–][А-ЯҐЇЄІ][а-яґіїє'`ʼ]?[ \t]*?\.\s*?)?){1,3}
[А-ЯҐЇЄІ]['`ʼа-яґіїє]+(?:[-−–][А-ЯҐЇЄІ]['`ʼа-яґіїє]+)?
|
(?:[A-Z][a-z]?\s*?\.\s*?(?:[-−–][A-Z][a-z]?[ \t]*?\.\s*?)?){1,3}
[A-Z][a-z]+(?:[-−–][A-Z][a-z]+)?
|
[А-ЯҐЇЄІ][а-яґіїє'`ʼ]+\s*?(?:[-−–][А-ЯҐЇЄІ]['`ʼа-яґіїє]+)?
(?:\s*?[А-ЯҐЇЄІ]['`ʼа-яґіїє]?\s*?\.(?:[-−–][А-ЯҐЇЄІ]['`ʼа-яґіїє]?\s*?\.)?){1,3}
|
[A-Z][a-z]+\s*?(?:[-−–][A-Z][a-z]+)?
(?:\s*?[A-Z][a-z]?\s*?\.(?:[-−–][A-Z][a-z]?\s*?\.)?){1,3}
|
(?<=\s)[А-ЯҐЇЄІ'`ʼ]+\s[А-ЯҐЇЄІ][а-яґіїє'`ʼ]+(?=\W)
|
\b[A-Z]+\s*?[A-Z][a-z]+(?=\W)
|
[А-ЯҐЇЄІ][а-яґіїє'`ʼ]+\ +?[А-ЯҐЇЄІ'`ʼ]{2,}(?=[,.])
|
[A-Z][a-z]+\s?[A-Z]{2,}(?=\b)
|
(?<![-−–])(?:(?:[А-ЯҐЇЄІ][а-яґіїє'`ʼ]+(?:[-−–][А-ЯҐЇЄІ][ʼ`'а-яґіїє]+){0,3}|[A-Z][a-z]+(?:[-−–][A-Z][a-z]+){0,3})\s?){2}
)
(?!”)""")
        return self.get_it(name_pattern, part_of_text, list_output=True, replace=True)

    def get_title(self, part_of_text: str):
        title_pattern = re.compile(r"""(?x)
(?<![a-zа-я].|.[a-zа-я])(?<=\n(?!УДК))\t?
[«“\"(]?[-−–А-ЯЇЄҐІ'’]+\s(?:[«“\"(]?[«“\"(]?[-−–\dА-ЯЇЄҐІA-Z'’/]+[»”\")]?[-−–:,?!.'’)]?\s)*[«“\"(]?[-−–\dА-ЯЇЄҐІ'’A-Z)]+?[»”\"?)]*?
(?=\n\s*[А-ЯЇЄҐІ]?\s?[()а-яіє'’їґ])
|
(?<![a-zа-я].|.[a-zа-я])(?<=\n)\t?
[«“\"(]?\b[A-Z](?![OО][IІ]|D[СC])[-−–\dA-Z]+(?:\s[«“\"(]?[^a-z]+?[»”\")]?[-−–:,?!.'’)]?)?
(?=\n\s?[A-Z]?[a-z])""")
        return self.get_it(title_pattern, part_of_text, replace=False)

    def get_year(self, parts_of_text: list):
        year_pattern = re.compile(r"20[0-9]{2}(?![-−–).])")
        return self.get_it(year_pattern, parts_of_text, replace=True, integer=True)

    def get_udc(self, parts_of_text: list) -> tuple:
        udc_pattern = re.compile(r"(?<=(?:УДК|UDC)\s|(?:ДК|DC):\s)\(?[0-9]+.+?\b(?=\s|$)")
        udc, parts_of_text = self.get_it(udc_pattern, parts_of_text, replace=False)
        return udc.strip(), parts_of_text

    def get_institution(self, parts_of_text: list) -> tuple:
        institution_pattern = re.compile(r"""(?x)(?:(?<=[\n \t])|^)(?:
(?:(?:[А-ЯЇЄІҐ« ]+)?
(?:(?:аціональн|ержавн)[а-яіїєґ]+\s(?:[-−–«а-яіїєґ»]+\s)?
|
[-−–«а-яіїєґ»]+\s(?:національн|державн)[а-яіїєґ]+\s(?:[«а-яіїєґ»]+\s)?)?
(?:[Аа]кадем|[Іі]нстит|[Уу]нівер).+?(?:\s«?[А-ЯЇЄІҐ]?[а-яіїєґ»]+)+?(?:\s[А-ЯІЄЇҐа-яієїґ». ]+)?
|
[А-ЯІЄЇҐ]+\sімені\s[А-ЯІЄЇҐа-яієїґ ]+?)
(?=[,\n]|$|\ Науков|(?<!ім)\.)
|
(?<=\s)[-−–А-ЯІЄЇҐа-яієїґ» ]+?\sуніверситет(?:\sім(?:ені|\.)?\s[А-ЯІЄЇҐа-яієїґ]+?)+?(?=[,\s])
|
[НH][аa][УY][КK][МM][АA]
|
[А-ЯЇЄІҐ« ]+(?:[-−–«а-яіїєґ»]+\s)+?НАН\ України(?=[,\s]))""")
        institution, parts_of_text = self.get_it(institution_pattern, parts_of_text, replace=True, list_output=True)
        if not institution:
            return institution, parts_of_text
        if len(institution) > 1:
            if len(institution[1]) > len(institution[0]):
                return institution[1].strip(), parts_of_text
        return institution[0].strip(), parts_of_text

    def get_doi(self, parts_of_text):
        doi_pattern = re.compile(r"(?i)(?:(?<=doi\.org/)|(?<=doi ))\(?[0-9]+[^удк\n ]+")
        doi, parts_of_text = self.get_it(doi_pattern, parts_of_text, replace=True)
        if doi != '':
            doi = 'https://doi.org/' + doi.strip()
        return doi, parts_of_text

    def get_annotation(self, parts_of_text, ukrainian=0, english=0, russian=0):
        annotation_ukrainian_pattern = re.compile(r"""(?xm)(?<=[А-ЯІЄЇҐA-Z]{2}..\n)
        \t(?:Анотація\.\ ?\s)?(?:[А-ЯІЄЇҐ](?:\s?\S+){4,}\s+?)+(?=\s*?$)""")
        annotation_english_pattern = re.compile(r"""(?x)(?:(?:Summary|Abstract|Annotation)?\.?\s+?
                                                [Bb]ackground:|(?<=[A-Z]{3}.\n))(?:(?:\s+?\S+){4,}?)+\.""")
        annotation_russian_pattern = re.compile(r"""(?x)(?<=\n)\t?(?:Аннотация\.\s*?)?
        [А-ЯЫЭЪ]\s?[а-яыэъ]+?(?:\s[«“\"(]?[А-ЯЫЭЪа-яыэъ]+[»”\")]?[-.,:?!'’]?){4,}\.(?=\s+?Ключевые\ слова)""")
        ukrainian_annotation = ""
        english_annotation = ""
        russian_annotation = ""
        if ukrainian == 0:
            ukrainian_annotation, parts_of_text = \
                self.get_it(annotation_ukrainian_pattern, parts_of_text, replace=True)
            if len(ukrainian_annotation) == 0:
                if (parts_of_text[-1] == "" or parts_of_text[-1] == "\n") and len(parts_of_text) > 1:
                    ukrainian_annotation = parts_of_text[-2]
                else:
                    ukrainian_annotation = parts_of_text[-1]
        if english == 0:
            english_annotation, parts_of_text = self.get_it(annotation_english_pattern, parts_of_text)
        if russian == 0 and self.list_of_keywords_russian != ['']:
            # print(parts_of_text)
            russian_annotation, parts_of_text = self.get_it(annotation_russian_pattern, parts_of_text)
        if type(parts_of_text) == str:
            parts_of_text = parts_of_text.split("\n")
        return ukrainian_annotation, english_annotation, russian_annotation, parts_of_text

    def get_abbreviations(self, part_of_text):
        abbreviations_ukrainian_pattern = re.compile(r"""(?x)
(?:(?<=\t[Уу]мовні\s[Сс]корочення\n)|(?<=\t[Уу]мовні\s[Сс]корочення:\n)|
(?<=\tС(?:писок|ПИСОК)\s[Уу]мовних\s[Сс]корочень\n)|
(?<=\tС(?:писок|ПИСОК)\s[Уу]мовних\s[Сс]корочень:\n)|
(?<=\tС(?:писок|ПИСОК)\s[Сс]корочень\n)|(?<=\tС(?:писок|ПИСОК)\s[Сс]корочень:\n))
\S+(?:\s+?\S+)+?
(?=(?:(?:В(?:икористані|ИКОРИСТАНІ))?\s?[Дд](?:жерела|ЖЕРЕЛА)|
С(?:писок|ПИСОК)\s(?:(?:використаних|ВИКОРИСТАНИХ)?\s?(?:джерел|ДЖЕРЕЛ)\s?(?:[Іі]люстративного\s[Мм]атеріалу)?|
[Лл]ітератури|ЛІТЕРАТУРИ)|Література|ЛІТЕРАТУРА|А(?:нотація|НОТАЦІЯ)|(?:L(?:ist|IST)\s(?:of|Of|OF)\s)?
(?:[Ss]ources|SOURCES|[Rr]eferences|REFERENCES|[Aa]bbreviations|ABBRAVIATIONS)|S(?:ummary|UMMARY)|
A(?:bstract|BSTRACT)|A(?:nnotation|NNOTATION)|Background|Vitae|(?:Стаття\s)?[Нн]адійшла до)[:.]?)""")
        abbreviations_english_pattern = re.compile(r"""(?x)
(?:(?<=\tL(?:ist|IST)\s(?:of|Of|OF)\s[Aa](?:bbreviations|BBRAVIATIONS)\n)|
(?<=\tL(?:ist|IST)\s(?:of|Of|OF)\s[Aa](?:bbreviations|BBRAVIATIONS):\n)|
(?<=\t[Aa](?:bbreviations|BBRAVIATIONS)\n)|
(?<=\t[Aa](?:bbreviations|BBRAVIATIONS):\n))
\S+(?:\s+?\S+)+?
(?=(?:(?:В(?:икористані|ИКОРИСТАНІ))?\s?
[Дд](?:жерела|ЖЕРЕЛА)|С(?:писок|ПИСОК)\s(?:(?:використаних|ВИКОРИСТАНИХ)?\s?(?:джерел|ДЖЕРЕЛ)\s?
(?:[Іі]люстративного\s[Мм]атеріалу)?|(?:[Уу]мовних\s)?[Сс]корочень|[Лл]ітератури|ЛІТЕРАТУРИ)|
[Уу]мовні\s[Сс]корочення|Література|ЛІТЕРАТУРА|А(?:нотація|НОТАЦІЯ)|(?:L(?:ist|IST)\s(?:of|Of|OF)\s)?
(?:[Ss](?:ources|OURCES)|[Rr](?:eferences|EFERENCES))|S(?:ummary|UMMARY)|A(?:bstract|BSTRACT)|
A(?:nnotation|NNOTATION)|Background|Vitae|(?:Стаття\s)?[Нн]адійшла\sдо)[:.]?)""")
        abbreviations_ukrainian, part_of_text = self.get_it(abbreviations_ukrainian_pattern, part_of_text)
        abbreviations_english, part_of_text = self.get_it(abbreviations_english_pattern, part_of_text)
        return abbreviations_ukrainian, abbreviations_english

    def get_sources(self, part_of_text):
        sources_ukrainian_pattern = re.compile(r"""(?x)
(?:(?<=\tВ(?:икористані|ИКОРИСТАНІ)\s[Дд](?:жерела|ЖЕРЕЛА)\n)|
(?<=\tВ(?:икористані|ИКОРИСТАНІ)\s[Дд](?:жерела|ЖЕРЕЛА):\n)|
(?<=\t[Дд](?:жерела|ЖЕРЕЛА)\n)|(?<=[Дд](?:жерела|ЖЕРЕЛА):\n)|(?<=\tС(?:писок|ПИСОК)\s(?:джерел|ДЖЕРЕЛ)\n)|
(?<=\tС(?:писок|ПИСОК)\s(?:джерел|ДЖЕРЕЛ):\n)|
(?<=\tС(?:писок|ПИСОК)\s(?:використаних|ВИКОРИСТАНИХ)\s(?:джерел|ДЖЕРЕЛ)\n)|
(?<=\tС(?:писок|ПИСОК)\s(?:використаних|ВИКОРИСТАНИХ)\s(?:джерел|ДЖЕРЕЛ):\n)|
(?<=\tС(?:писок|ПИСОК)\s(?:джерел|ДЖЕРЕЛ)\s[Іі]люстративного\s[Мм]атеріалу\n)|
(?<=\tС(?:писок|ПИСОК)\s(?:джерел|ДЖЕРЕЛ)\s[Іі]люстративного\s[Мм]атеріалу:\n))
\S+(?:\s+?\S+)+?
(?=\n\t(?:[Уу]мовні\s[Сс]корочення|С(?:писок|ПИСОК)\s(?:(?:[Уу]мовних\s)?[Сс]корочень|
[Лл]ітератури|ЛІТЕРАТУРИ)|Література|ЛІТЕРАТУРА|А(?:нотація|НОТАЦІЯ)|(?:L(?:ist|IST)\s(?:of|Of|OF)\s)?
(?:[Aa](?:bbreviations|BBRAVIATIONS)|[Rr](?:eferences|EFERENCES)|[Ss](?:ources|OURCES))|S(?:ummary|UMMARY)|
A(?:bstract|BSTRACT)|A(?:nnotation|NNOTATION)|Background|Vitae|(?:Стаття\s)?[Нн]адійшла\sдо)[:.]?\n|\s*?\n[A-Z]{2,})""")
        sources_english_pattern = re.compile(r"""(?x)
(?:(?<=\tL(?:ist|IST)\s(?:of|Of|OF)\s[Ss](?:ources|OURCES)\n)|
(?<=\tL(?:ist|IST)\s(?:of|Of|OF)\s[Ss](?:ources|OURCES):\n)
|(?<=\t[Ss](?:ources|OURCES)\n)|(?<=\t[Ss](?:ources|OURCES):\n))
\S+(?:\s+?\S+)+?
(?=\n\t(?:(?:В(?:икористані|ИКОРИСТАНІ))?\s?[Дд](?:жерела|ЖЕРЕЛА)|С(?:писок|ПИСОК)\s
(?:(?:використаних|ВИКОРИСТАНИХ)?\s?(?:джерел|ДЖЕРЕЛ)\s?(?:[Іі]люстративного\s[Мм]атеріалу)?|(?:[Уу]мовних\s)?
[Сс]корочень|[Лл]ітератури|ЛІТЕРАТУРИ)|[Уу]мовні\s[Сс]корочення|Література|ЛІТЕРАТУРА|А(?:нотація|НОТАЦІЯ)|
(?:L(?:ist|IST)\s(?:of|Of|OF)\s)?(?:[Aa]bbreviations|ABBRAVIATIONS|[Rr]eferences|REFERENCES)|S(?:ummary|UMMARY)|
A(?:bstract|BSTRACT)|A(?:nnotation|NNOTATION)|Background|Vitae|(?:Стаття\s)?[Нн]адійшла\sдо)[:.]?\n|\s*?\n[A-Z]{2,})""")
        sources_ukrainian, part_of_text = self.get_it(sources_ukrainian_pattern, part_of_text)
        sources_english, part_of_text = self.get_it(sources_english_pattern, part_of_text)
        return re.split(r"(?<=\d [сc]\.) (?=\[A-ZА-ЯІЄЇҐ])", sources_ukrainian), \
            re.split(r"(?<=\d\. Print\.)\s", sources_english)

    def get_references(self, part_of_text):
        references_ukrainian_pattern = re.compile(r"""(?x)
(?:(?<=\tС(?:писок|ПИСОК)\s[Лл](?:ітератури|ІТЕРАТУРИ)\n)|(?<=\tС(?:писок|ПИСОК)\s[Лл](?:ітератури|ІТЕРАТУРИ):\n)|
(?<=\t(?:Література|ЛІТЕРАТУРА)\n)|(?<=\t(?:Література|ЛІТЕРАТУРА):\n))
\S+(?:\s+?\S+)+?
(?=\n\t(?:(?:В(?:икористані|ИКОРИСТАНІ))?\s?[Дд](?:жерела|ЖЕРЕЛА)|С(?:писок|ПИСОК)\s
(?:(?:використаних|ВИКОРИСТАНИХ)?\s?(?:джерел|ДЖЕРЕЛ)\s?(?:[Іі]люстративного\s
[Мм]атеріалу)?|[Уу]мовних\s)?[Сс]корочень|[Уу]мовні\s[Сс]корочення|Література|
ЛІТЕРАТУРА|А(?:нотація|НОТАЦІЯ)|(?:L(?:ist|IST)\s(?:of|Of|OF)\s)?(?:[Ss](?:ources|OURCES)|
[Aa](?:bbreviations|BBRAVIATIONS)|[Rr](?:eferences|EFERENCES))|S(?:ummary|UMMARY)|
A(?:bstract|BSTRACT)|A(?:nnotation|NNOTATION)|Background|Vitae|(?:Стаття\s)?[Нн]адійшла\sдо)[:.]?\n|\s*?\n[A-Z]{2,})""")
        references_english_pattern = re.compile(r"""(?x)
(?:(?<=\tL(?:ist|IST)\s(?:of|Of|OF)\s[Rr](?:eferences|EFERENCES)\n)|
(?<=\tL(?:ist|IST)\s(?:of|Of|OF)\s[Rr](?:[eе]f[eе]r[eе]n[сc][eе]s|EFERENCES):\n)|
(?<=\t[Rr](?:[eе]f[eе]r[eе]n[сc][eе]s|EFERENCES)\n)|(?<=\t[Rr](?:[eе]f[eе]r[eе]n[сc][eе]s|EFERENCES):\n))
\t?\S+(?:\s+?\S+)+?
(?=\n\t(?:(?:В(?:икористані|ИКОРИСТАНІ))?\s?[Дд](?:жерела|ЖЕРЕЛА)|С(?:писок|ПИСОК)\s
(?:(?:використаних|ВИКОРИСТАНИХ)?\s?(?:джерел|ДЖЕРЕЛ)\s?(?:[Іі]люстративного\s[Мм]атеріалу)?|
(?:[Уу]мовних\s)?[Сс]корочень|[Лл]ітератури|ЛІТЕРАТУРИ)|[Уу]мовні\s[Сс]корочення|Література|ЛІТЕРАТУРА|
А(?:нотація|НОТАЦІЯ)|(?:L(?:ist|IST)\s(?:of|Of|OF)\s)?(?:[Ss]ources|SOURCES|[Aa]bbreviations|ABBRAVIATIONS)|
S(?:ummary|UMMARY)|A(?:bstract|BSTRACT)|A(?:nnotation|NNOTATION)|Background|Vitae|
(?:Стаття\s)?[Нн]адійшла\sдо)[:.]?|\n\t(?:[A-Z][a-z]+(?:[-−–][A-Z][a-z]+)?\s?){2,3},|\s*?\n[A-Z]{2,})""")
        references_ukrainian, part_of_text = self.get_it(references_ukrainian_pattern, part_of_text)
        references_english, part_of_text = self.get_it(references_english_pattern, part_of_text)
        return re.split(r"(?<=\d [сc]\.|[-−–\d]{2}\d\.)\n(?=\d|\t)", references_ukrainian), \
            re.split(r"(?<=\)\.)\n(?=\d)", references_english)

    def get_journal_type(self):
        if self.folder_counter == 1:
            return "scientific"
        return "predatory"

    def parse_it(self):
        if self.text == "":
            return self.text, self.metadata

        self.list_of_keywords_ukrainian, self.list_of_keywords_english, self.list_of_keywords_russian \
            = self.get_keywords()
        reduced_keywords_pattern = re.compile(r"\t?(?:[KКк]люч[оoеe]в[іi] [сc]л[оo]в[аa]|Key ?words) ?\.")
        reduced_literature_pattern = re.compile(r"""(?ix)
\n(?=\t?(?:Література|Джерела|Список\sвикористаних\sджерел|
Список\sлітератури|List\sof\sSources|References)(?!\s[-−–]))""")

        split_list = reduced_keywords_pattern.split(self.text, 1)

        if split_list[0] == "" or split_list[0] == "\n":
            split_list.pop(0)
        title_in_ukrainian, upper_info = self.get_title(split_list[0])
        print("HERE")

        # print(split_list[0])
        self.annotation_ukrainian, self.annotation_english, self.annotation_russian, upper_info = self.get_annotation(split_list[0])

        self.journal, upper_info[0] = self.get_journal(upper_info[0])
        # print(upper_info)
        self.name_of_institution, upper_info = self.get_institution(upper_info)
        self.list_of_authors, upper_info = self.get_authors_name(upper_info)
        self.year_of_publication, upper_info = self.get_year(upper_info)
        self.article_udc, upper_info = self.get_udc(upper_info)
        self.article_doi, upper_info = self.get_doi(upper_info)

        # print(self.annotation_ukrainian)
        # print(split_list[1])
        split_list = reduced_literature_pattern.split(split_list[1], 1)
        # print(len(split_list))
        self.text = split_list[0].strip()
        # print(split_list[1])

        lower_info = reduced_keywords_pattern.split(split_list[1])[0]

        annotations = self.get_annotation(lower_info, len(self.annotation_ukrainian),
                                          len(self.annotation_english), len(self.annotation_russian))
        if len(self.annotation_ukrainian) == 0:
            self.annotation_ukrainian = annotations[0]
        if len(self.annotation_english) == 0:
            self.annotation_english = annotations[1]
        if len(self.annotation_russian) == 0:
            self.annotation_russian = annotations[2]

        self.abbreviations_ukrainian, self.abbreviations_english = self.get_abbreviations(lower_info)
        self.list_of_sources_ukrainian, self.list_of_sources_english = self.get_sources(lower_info)
        self.list_of_references_ukrainian, self.list_of_references_english = self.get_references(lower_info)

        self.article_title.append(title_in_ukrainian)
        title_in_english, lower_info = self.get_title(lower_info)
        if title_in_english != '':
            self.article_title.append(title_in_english)

        self.metadata["journal"] = self.journal.strip(". \n«»")
        self.metadata["journal type"] = self.get_journal_type()
        self.metadata["author"] = self.list_of_authors
        self.metadata["institution"] = self.name_of_institution
        self.metadata["title"] = self.article_title
        self.metadata["doi"] = self.article_doi
        self.metadata["year"] = self.year_of_publication
        self.metadata["udc"] = self.article_udc
        self.metadata["keywords"]["in Ukrainian"] = self.list_of_keywords_ukrainian
        self.metadata["keywords"]["in English"] = self.list_of_keywords_english
        self.metadata["keywords"]["in russian"] = self.list_of_keywords_russian
        self.metadata["annotation"]["in Ukrainian"] = self.annotation_ukrainian
        self.metadata["annotation"]["in English"] = self.annotation_english
        self.metadata["annotation"]["in russian"] = self.annotation_russian
        self.metadata["abbreviations"]["in Ukrainian"] = self.abbreviations_ukrainian
        self.metadata["abbreviations"]["in English"] = self.abbreviations_english
        self.metadata["sources"]["in Ukrainian"] = self.list_of_sources_ukrainian
        self.metadata["sources"]["in English"] = self.list_of_sources_english
        self.metadata["references"]["in Ukrainian"] = self.list_of_references_ukrainian
        self.metadata["references"]["in English"] = self.list_of_references_english
        return self.text, self.metadata
