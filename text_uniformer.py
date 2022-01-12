# !/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from pathlib import Path, PurePosixPath
from build_a_corpus import iterate


class UniformText:
    def __init__(self, text: str):
        self.text = re.sub("­", "-", text)

        lower_cyrillic_pattern = re.compile(r"(?<=.[а-яієїґ]|[-–а-яієїґ] )([ioeypacx])(?= ?[а-яієїґ])")
        lower_latin_to_cyrillic = {"i": "і",
                                   "o": "о",
                                   "e": "е",
                                   "y": "у",
                                   "p": "р",
                                   "a": "а",
                                   "c": "с",
                                   "x": "х"}
        upper_cyrillic_pattern = re.compile(r"(?<=.[А-ЯІЄЇҐ]|[А-ЯІЄЇҐ] )([AXECBTHMKIOP])(?= ?[А-ЯІЄЇҐ])")
        upper_latin_to_cyrillic = {"A": "А",
                                   "X": "Х",
                                   "E": "Е",
                                   "C": "С",
                                   "B": "В",
                                   "T": "Т",
                                   "H": "Н",
                                   "M": "М",
                                   "K": "К",
                                   "I": "І",
                                   "O": "О",
                                   "P": "Р"}
        lower_latin_pattern = re.compile(r"(?<=.[a-z]|[a-z] )([іоеурасх])(?= ?[a-z])")
        lower_cyrillic_to_latin = {"і": "i",
                                   "о": "o",
                                   "е": "e",
                                   "у": "y",
                                   "р": "p",
                                   "а": "a",
                                   "с": "c",
                                   "х": "x"}
        upper_latin_pattern = re.compile(r"(?<=.[A-Z]|[A-Z] )([АХЕСВТНМКІОР])(?= ?[A-Z])")
        upper_cyrillic_to_latin = {"А": "A",
                                   "Х": "X",
                                   "Е": "E",
                                   "С": "C",
                                   "В": "B",
                                   "Т": "T",
                                   "Н": "H",
                                   "М": "M",
                                   "К": "K",
                                   "І": "I",
                                   "О": "O",
                                   "Р": "P"}
        letter_patterns = (lower_latin_pattern, upper_latin_pattern, lower_cyrillic_pattern, upper_cyrillic_pattern)
        letter_conversions = (lower_cyrillic_to_latin, upper_cyrillic_to_latin, lower_latin_to_cyrillic, upper_latin_to_cyrillic)
        broken_word_pattern = re.compile(r"""(?x)
        (?<=[a-zа-яієїґя́á])\s(?=[a-zа-яієїґя́á][–-]\s?\n+)|
        (?<=[a-zа-яієїґя́á][–-])(?:[ \t]\n*|
        [ \t?\n])(?=[А-ЯІЇЄҐA-Z0-9])|©.+(?=\n)""")
        hyphen_pattern = re.compile(r"(?<=[a-zа-яієїґя́á](?<![0-9]))[-–][ \t]\n*(?![А-ЯІЇЄҐA-Z])")
        footnote_pattern = re.compile(
            r"""(?x)\n\ *[0-9]+(?!\.)\ *
            (?!Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept?|Oct|Nov|Dec|[А-ЯІЇҐЄA-Z]{3,})
            [А-ЯІЇҐЄA-Z](?:.+\n?)+(?=\n\n)""")
        media_pattern = re.compile(r"""(?x)
        ((?:(?<!див\.\s)|(?<!\())(?:(?:Рис|Мал)(?:[ \t]|у?ю?нок)?|
        Діаг(?:[ \t]|рама)?|Табл?(?:[ \t]|иця)?|Пр(?:иклад)?|Фото|
        Графік|Ментальна карта)\.?[ \t]?(?:\d{1,2}[ \t]?\.?){1,2}
        [\s\S]+?(?=\n\n))""")
        no_hyphen_brakes_and_lists_pattern = re.compile(r"""(?x)
(?<=(?<![А-ЯЇЄҐІA-Z»'’”\"?!.]{3})[:!?\[\].…+\"\\/()”’'“&«»<>])
[ \t]*\n+
(?=(?![A-ZA-ZА-ЯІЄЇҐ]{2,}|[\[(][0-9]{1,2}[])]\s[A-Za-zА-ЯІЄЇа-яієїґ]+|
[0-9]{1,2}\.)[-–А-ЯІЄЇҐA-Z.\[+“\"\\/(&«<0-9])
|
(?<=(?<![А-ЯЇЄҐІA-Z»'’”\"?!.]{3})[-−–;:%\[\],…+\"\\/()”’'“&«»<>a-zа-яіїєґ])(?<!\s[Ss]ources|terature)
[ \t]*\n+
(?=(?![A-ZA-ZА-ЯІЄЇҐ]{2,}|[0-9]{1,2}\.|[\[(][0-9]{1,2}[])]\s[a-zA-ZА-ЯІЄЇа-яієїґ]+|
\ *Abstract[.:]?\s+Background|[ \t]*Background:\ [A-Z])[–“…\"\[\\/(&«<]?[A-ZA-ZА-ЯІЄЇҐ]?
[а-яієїґА-ЯІЄЇҐA-Za-z\\/)(\[+0-9 ….>;:%»”\"’']{2,})
|
(?<=№)
[ \t]*\n+
(?=[0-9])""")
        additional_broken_word_pattern = re.compile(r"(?<=[a-zа-яієїґя́á])[–-][ \t](?=[a-zа-яі єїґя́á])")
        multiple_spaces_tabs_inside_sentences_pattern = re.compile(r"""(?ix)
        (?<=[-–\w;:%!?\[\].,…+№\"\\/()”’'“&«‖|»<>А-ЯІЄЇҐ])\ {2,}|
        \t{1,}(?=[-–\w;:№%!?\[\].,…+|‖\"\\/()”’'“&«»<>А-ЯІЄЇҐ])""")
        spaces_before_paragraph_pattern = re.compile(r"(?<=\n) +(?=[(\[“«<А-ЯІЄЇҐA-Z0-9])")
        finish_paragraph_pattern = re.compile(r"""(?x)
(?<![\dА-ЯЇЄҐІA-Z»'’”\")?!.]{4})\ *\n+
(?!\t|[0-9]{1,2}\.|[\[(][0-9]{1,2}[])]\s[a-zA-ZА-ЯІЄЇа-яієїґ]+|
(?:[«“\"(]?[-\dА-ЯЇЄҐІA-Z]{1,}[»”\")]?[-:,?!.'’)]?\s){4,}|
Abstract[.:]?\s+Background|\s*Background:\ [A-Z])""")
        list_without_tabs_pattern = re.compile(
            r"(?<=\n)\t(?=[0-9]{1,2}\.\s)|(?<= )\t(?=[A-ZА-ЯІЄЇҐ][A-Za-zА-ЯІЄЇҐа-яієїґ]+)")
        list_pattern = re.compile(r"""(?x)(
(?:(?<!Рис\.\s)|(?<![0-9]{2})|(?<!Vol\.\s)|(?<!\w|\d))(?<=.\n|[,:;]\s)
\n?(?:[0-9]{1,2}\.){1,2}\s\[?[-–A-Za-zА-ЯІЄЇҐа-яієїґ’'` ]+?[\s\S]+?(?:[;:,.ій]|та|або|and|or)?
(?:[(0-9]{1,2}\.?\s(?:Print|С.+|кн.+|kn.+|Вип.+|/.+|№.+|x.+)\.?)??
(?!\d{1,2}\.\s(?:Print\.|[CС]\.?|Вип\.|№|Харків|Kyiv))(?=(?<!\d{2})\d{1,2}\.\s[^(\d]|\n|$)
|
(?<!(?<=[^:;,]\s)|(?<=[,№]\s)|(?<=[0-9]{2})|(?<=\w{2})|(?<=.[-\d]))
\n?[0-9]{1,2}\)(?=\s[^0-9\\])\s?[\s\S]+?(?:[.;]?\s|[.;]\s?)(?:[;:,ій]|та|чи|або|and|or)?
(?=\n{2,}|\n\t|(?<!\s\d[).].|\s\d{2}[).])[A-ZА-ЯІЄЇҐ][-−–A-Za-zА-ЯІЄЇҐа-яієїґ’'` ]+?[\s\S]+?|[0-9]{1,2}[).])
|
(?<![\wА-ЯІЄЇҐа-яієїґ])
(?<=[:;]\s|.“|,\s)\n?[абвгґдеєжзиіїклмн]\)(?=\s?[^\\/,.][^0-9])
\s\[?[-−–A-Za-zА-ЯІЄЇҐа-яієїґ’'` ]+?[\s\S]+?[,.;]\s?(?:[,ій]|та|або|and|or)?
(?=\n+\t?|.*[абвгґдеєжзиіїклмн]\)|[A-ZА-ЯІЄЇҐ][-−–A-Za-zА-ЯІЄЇҐа-яієїґ’'`]+)
|
(?<=.[:;.]\s|,\ \n|[-−–A-Za-zА-ЯІЄЇҐа-яієїґ’'`)\]]{2}\s)
\n?[•●*]\s+[-−–A-Za-zА-ЯІЄЇҐа-яієїґ’'` ]+?[\s\S]+?[.;]?
(?=\n{2,}|\n\t|\s*(?:[•●*]|\d[).])\s+[-−–A-Za-zА-ЯІЄЇҐа-яієїґ’'` ]+|\.\ [A-ZА-ЯІЄЇҐ][-−–A-Za-zА-ЯІЄЇҐа-яієїґ’'`]+|$)
|
(?<!\d\.\s)(?<=.[:;.]\s|,\ \n)
\n?[-−–]\s+(?![A-ZА-ЯІЄЇҐ]\.\s[\d:])[-–A-Za-zА-ЯІЄЇҐа-яієїґ’'` ]+?[\s\S]+?[.;]?
(?=\n{2,}|\n\t|\s*[-−–]\s+[-−–A-Za-zА-ЯІЄЇҐа-яієїґ’'` ]+|$)
|
(?<=\n)
[ \t]*?(?:[ІI]{1,3}|[ІI]?V(?:[ІI]{1,3})?|[ІI]?[XХ](?:[ІI]{1,3})?)\.\ [-−–A-Za-zА-ЯІЄЇҐа-яієїґ’'` ]+?(?=\n)
)""")
        lighted_list_pattern = re.compile(r"""(?x)(
\n?(?:[0-9]{1,2}\.){1,2}\s\[?[A-ZА-ЯІЄЇҐ][A-Za-zА-ЯІЄЇҐа-яієїґ’'` ]+?[\s\S]+?(?:[;:,.ій]|та|або|and|or)?
(?:[(0-9]{1,2}\.?\s(?:Print|С.+|кн.+|kn.+|Вип.+|/.+|№.+|x.+)\.?)??
|
\n?[0-9]{1,2}\)(?=\s[^0-9/\\])\s?[\s\S]+?(?:[.;]?\s|[.;]\s?)(?:[;:,ій]|та|чи|або|and|or)?
|
\n?[абвгґдеєжзиіїклмн]\)\s\[?[A-Za-zА-ЯІЄЇҐа-яієїґ’'` ]+?[\s\S]+?[,.;]\s?(?:[,ій]|та|або|and|or)?\s?
|
\n?[•●*]\s+[A-Za-zА-ЯІЄЇҐа-яієїґ’'` ]+?[\s\S]+?[.;]?
|
\n?[-−–]\s+[A-Za-zА-ЯІЄЇҐа-яієїґ’'` ]+?[\s\S]+?[.;]?
|
\n?[ \t]*?(?:[ІI]{1,3}|[ІI]?V(?:[ІI]{1,3})?|[ІI]?[XХ](?:[ІI]{1,3})?)\.\ [-−–A-Za-zА-ЯІЄЇҐа-яієїґ’'` ]+?(?=\n)
)""")
        structure_parts_pattern = re.compile(r"""(?x)((?<!.[А-ЯІЄЇҐа-яієїґa-zA-Z]\ |[А-ЯІЄЇҐа-яієїґa-zA-Z][:;,]\ )
(?:(?:В(?:икористан[іi]|ИКОРИСТАНІ)\ )?[Дд](?:жерела|ЖЕРЕЛА)
|
С(?:писок|ПИСОК)\ (?:використаних\ |ВИКОРИСТАНИХ\ )?(?:джерел\ |ДЖЕРЕЛ\ ?)(?:[Ііi]люстративного\ [Мм]атер[іi]алу)?
|
(?:Л[іi]тература|ЛІТЕРАТУРА)
|
С(?:писок|ПИСОК)\ (?:(?:[Лл][іi]тератури|ЛІТЕРАТУРИ)|(?:[Уу]мовних\ )?[Сс]корочень)
|
А(?:нотац[іi]я|НОТАЦІЯ)
|
[Уу]мовн[іi]\ [Сс]корочення
|
[Rr](?:eferences|EFERENCES)
|
L(?:ist|IST)\ (?:of|Of)\ (?:[Ss](?:ources|OURCES)
|
[Aa](?:bbreviations|BBRAVIATIONS))
|
S(?:ummary|UMMARY)
|
A(?:bstract|BSTRACT)
|
A(?:bbreviations|BBRAVIATIONS)
|
A(?:nnotation|NNOTATION)
|Background
|Purpose
|Results
|Discussion
|Vitae)
[:.]?(?!\s[«“\"]?[а-яієїґa-z…]|\s[А-ЯІЄЇҐ])(?=[ \n](?!Web|Print))
|(?:[Kk][еe][yу]\ ?w[оo]rds|[KКк]люч[оo]в[іi]\ [сc]л[оo]в[аa]|[Кк]люч[еe]вы[еe]\ [сc]л[оo]в[аa]):[\s\S]+?(?:\.|
(?=Vitae))|(?:UDC|УДК)\s.+?(?=\s)|(?:DOI|doi)\s.+?(?=\s))(?!\s[-−–])""")
        lighted_structure_parts_pattern = re.compile(r"""(?x)(
(?:(?:В(?:икористані|ИКОРИСТАНІ)\s)?[Дд](?:жерела|ЖЕРЕЛА)
|
С(?:писок|ПИСОК)\s(?:використаних\s|ВИКОРИСТАНИХ\s)?(?:джерел\s|ДЖЕРЕЛ\s?)(?:[Іі]люстративного\s[Мм]атеріалу)?
|
(?:Л[іi]тература|ЛІТЕРАТУРА)
|
С(?:писок|ПИСОК)\s(?:(?:[Лл][іi]тератури|ЛІТЕРАТУРИ)|(?:[Уу]мовних\s)?[Сс]корочень)
|
А(?:нотац[іi]я|НОТАЦІЯ)
|
[Уу]мовн[іi]\s[Сс]корочення
|
[Rr](?:eferences|EFERENCES)
|
L(?:ist|IST)\s(?:of|Of)\s(?:[Ss](?:ources|OURCES)
|
[Aa](?:bbreviations|BBRAVIATIONS))
|
S(?:ummary|UMMARY)
|
A(?:bstract|BSTRACT)
|
A(?:bbreviations|BBRAVIATIONS)
|
A(?:nnotation|NNOTATION)
|Background
|Purpose
|Results
|Discussion
|Vitae)
[:.]?
|(?:[Kk][еe][yу]\ ?w[оo]rds|[KКк]люч[оo]в[іi]\ [сc]л[оo]в[аa]|[Кк]люч[еe]вы[еe]\s[сc]л[оo]в[аa]):[\s\S]+?\.?
|(?:UDC|УДК)\s|(?:DOI|doi)\s)""")
        title_pattern = re.compile(r"""(?x)((?<=\n)\s*?(?!ORCID|DOI|UDC|[А-ЯЇЄҐІA-ZĆ][.\d]|\d+[).]|[(\[])
        (?:[«“\"(]?(?:[-–А-ЯЇЄҐІA-ZĆ./ʼ’`']+|\d{1,2})[»”\")]?[-:,?!.'’)]?\s\n?){5,}
        (?=\s?\n|\s?[-\dА-ЯЇЄҐІA-Z]+(?:\s+?[-А-ЯЇЄҐІA-Z])?[а-яієїґa-z]+))""")

        for p in range(len(letter_patterns)):
            while letter_patterns[p].search(self.text):
                letter = letter_patterns[p].search(self.text)[0]
                self.text = letter_patterns[p].sub(letter_conversions[p][letter], self.text, count=1)

        self.text = broken_word_pattern.sub("", self.text)
        self.text = hyphen_pattern.sub("", self.text)

        pre_footnotes = [footnote.strip('\n \t') for footnote in footnote_pattern.findall(self.text)]
        self.text = footnote_pattern.sub("", self.text)
        pre_media = [media.strip('\n \t') for media in media_pattern.findall(self.text)]
        self.text = media_pattern.sub("", self.text)

        footnotes = []
        for footnote in pre_footnotes:
            footnotes.append(finish_paragraph_pattern.sub(" ", multiple_spaces_tabs_inside_sentences_pattern.sub(
                " ", additional_broken_word_pattern.sub("", no_hyphen_brakes_and_lists_pattern.sub(" ", footnote)))))
        medias = []
        for media in pre_media:
            medias.append(finish_paragraph_pattern.sub(" ", multiple_spaces_tabs_inside_sentences_pattern.sub(
                    " ", additional_broken_word_pattern.sub("", no_hyphen_brakes_and_lists_pattern.sub(" ", media)))))

        self.text = additional_broken_word_pattern.sub("", self.text)
        self.text = multiple_spaces_tabs_inside_sentences_pattern.sub(" ", self.text)
        self.text = spaces_before_paragraph_pattern.sub("\t", self.text)
        self.text = list_without_tabs_pattern.sub("", self.text)
        list_of_patterns = (list_pattern, structure_parts_pattern)
        list_of_additional_patterns = (lighted_list_pattern, lighted_structure_parts_pattern)

        for counter in range(2):
            self.text = list_of_patterns[counter].split(self.text)
            text_split = []
            if len(self.text) == 0:
                continue
            added = False
            for text_passage in self.text:
                if text_passage == "":
                    continue
                if text_passage[0] == "\n":
                    text_split.append(text_passage)
                    continue
                if list_of_additional_patterns[counter].match(text_passage):
                    if counter == 0:
                        text_split.append(f"\n{text_passage}")
                        continue
                    if re.match(r"""(?x)
(?:Д(?:жерела|ЖЕРЕЛА)(?!\s[А-ЯІЄЇҐ]+)|С(?:писок|ПИСОК)\s(?:використаних|ВИКОРИСТАНИХ)\s?
(?:джерел|ДЖЕРЕЛ)|(?:Література|ЛІТЕРАТУРА)|С(?:писок|ПИСОК)\s
(?:літератури|ЛІТЕРАТУРИ))[:.]?""", text_passage.strip()) and not added:
                        added = True
                        for media in medias:
                            text_split.append(f"\n\t{media}\n")
                        for footnote in footnotes:
                            text_split.append(f"\n\t{footnote}\n")
                    if counter == 1:
                        if text_passage.startswith("UDC") or text_passage.startswith("УДК") or text_passage.startswith("DOI"):
                            text_passage = "\n" + text_passage.strip("\n\t ") + "\n"
                        else:
                            text_passage = "\n\t"+text_passage.strip("\n\t ").capitalize()+"\n"
                        text_split.append(text_passage)
                else:
                    text_split.append(text_passage)
            self.text = "".join(text_split)

        # поділить залежно від кількости назв (укр, англ...)
        parts_of_text = title_pattern.split(self.text)
        # print(len(parts_of_text))

        if len(parts_of_text) == 3:
            self.text = parts_of_text.pop(2)
        elif len(parts_of_text) == 5:
            self.text = [parts_of_text.pop(2), "\n\n\n*SPLIT*\n\n\n", parts_of_text.pop(4-1)]
        else:
            self.text = parts_of_text
            # print(self.text)
            # print(len(self.text))
        # print(parts_of_text)
        self.text = [no_hyphen_brakes_and_lists_pattern.sub(" ", t) for t in self.text]
        self.text = ''.join(self.text)
        self.text = finish_paragraph_pattern.sub(" ", self.text)
        # print(len(parts_of_text))
        self.text = re.split("\*SPLIT\*", self.text)

        insert_indexes = [0, 1, 3, -1]
        counter = 0
        while parts_of_text:
            self.text.insert(insert_indexes[counter], parts_of_text.pop(0))
            if insert_indexes[counter] != -1:
                counter += 1

        # print(self.text)
        self.text = re.sub(r"[\n ]{2,}", "\n", re.sub(r"\n+\t+\n+", "\n", "\n".join(self.text))).strip('\n')
        # print(self.text)


def uniform_it(file):
    faulty_paths = []
    print(file)
    try:
        with open(file, "r+", encoding='utf-8') as current_file:
            article = UniformText(current_file.read())
            # print(article.text)
            current_file.seek(0)
            current_file.truncate(0)
            current_file.write(article.text)
    except UnicodeDecodeError or FileNotFoundError:
        faulty_paths.append(PurePosixPath(str(file)))
    return faulty_paths


def do_the_uniforming(folder_path):
    folder = Path(folder_path)
    broken_files = []
    if folder.exists():
        paths = iterate(folder)
        broken_files = [uniform_it(path) for path in paths]
    return [file for file in broken_files if file]


if __name__ == "__main__":
    # folder_good = "D:\\НАВЧАННЯ\\2 курс\\КУРСОВА\\Корпус\\Корпус хороших"
    # folder_bad = "D:\\НАВЧАННЯ\\2 курс\\КУРСОВА\\Корпус\\Корпус поганих"
    corpus_folder = "C:\\Users\\Bohdanka\\PycharmProjects\\Навчання\\2 курс\\Курсова\\Корпус наукових статей\\Corpus"
    print(do_the_uniforming(corpus_folder))

    # test = "C:\\Users\\Bohdanka\\PycharmProjects\\Навчання\\2 курс\\Курсова\\Корпус наукових статей\\Corpus\\Good articles\\Лінгвістичні студії ДоНУ\\2021\\Громко - Граматична система говірки за даними дескрипції. Іменникові форми.txt"
    #
    # file = "C:\\Users\\Bohdanka\\PycharmProjects\\Навчання\\2 курс\\Курсова\\Корпус наукових статей\\Corpus\\Good articles\\Українське мовознавство\\2018\\Лаврінець - Структурно-семантична специфіка та динаміка функціювання пасивних конструкцій.txt"
    # print(uniform_it(test))