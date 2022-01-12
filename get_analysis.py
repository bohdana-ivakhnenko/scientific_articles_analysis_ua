# !/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from abc import ABCMeta, abstractmethod
import pymorphy2
morph = pymorphy2.MorphAnalyzer(lang='uk')


def update(dictionary1: dict, dictionary2: dict) -> dict:
    for key, value in dictionary2.items():
        if key in dictionary1.keys():
            dictionary1[key] += value
        else:
            dictionary1[key] = value
    return {k: v for k, v in sorted(dictionary1.items(), key=lambda item: item[1], reverse=True)}


def get_average(lengths: list) -> float:
    if len(lengths) == 0:
        return 0
    average_length = 0
    for length in lengths:
        average_length += length
    return round(average_length / len(lengths), 2)


def get_median(lengths: list) -> float:
    if len(lengths) == 0:
        return 0
    lengths = sorted(lengths)
    index = len(lengths) / 2
    if len(lengths) % 2 == 0:
        return round((lengths[int(index-1)] + lengths[int(index)]) / 2, 2)
    return round(lengths[int(index-0.5)], 2)


class Analysis(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, text_passage: list):
        self.text_passage = text_passage

    @abstractmethod
    def parse_it(self, paragraph_counter=0, sentence_counter=0) -> dict:
        pass

    def get_it(self):
        return self


class Word:
    latin_alphabet = "qazwsxedcrfvtgbyhnujmikolpąęłńóśźćżčďéěňřšťúůž"
    cyrillic_alphabet = "’'`йфяцічувскамепинртгоьшлбщдюзжхєїґыёэўъ"
    letters = cyrillic_alphabet + latin_alphabet

    def __init__(self, word: str, pymorph=morph):
        self.word = word
        self.word_ = morph.parse(self.get_letters(hyphens=True))[0]
        self.morph = pymorph

    def get_letters(self, hyphens=False) -> str:
        letters_pattern = re.compile(r"""(?ix)
        (?:[qazwsxedcrfvtgbyhnujmikolpąęłńóśźćżčďéěňřšťúůžйфяцічувскамепинртгоьшлбщдюзжхєїґёыэўъ\d]
        |(?<!\b)’'`(?!,))+""")
        if hyphens:
            letters_pattern = re.compile(r"""(?ix)
            (?:[-−–qazwsxedcrfvtgbyhnujmikolpąęłńóśźćżčďéěňřšťúůžйфяцічувскамепинртгоьшлбщдюзжхєїґёыэўъ\d]
            |(?<!\b)’'`(?!,))+""")
        if letters_pattern.search(self.word):
            return letters_pattern.search(self.word)[0]
        return ""

    def get_length(self) -> int:
        length = 0
        for symbol in self.word:
            if symbol in self.letters or symbol in self.letters.upper():
                length += 1
        return length

    def is_a_functor(self) -> bool:
        # prepositions = ['в', 'на', 'з', 'за', 'до', 'по', 'у', 'біля', 'від', 'для', 'без', 'про', 'через', 'при',
        # 'над', 'з-за', 'з-під', 'під', 'близько', 'вглиб', 'крізь', 'поза', 'проміж']
        # conjunctions = ['і', 'й', 'що', 'так', 'хоча', 'коли', 'або', 'щоб', 'якщо', 'також',
        # 'чи', 'тобто', 'проте', 'немов', 'а', 'але', 'та', 'одначе']
        # particles = ['не', 'так', 'ж', 'же', 'навіть', 'би', 'б', 'або', 'лише', 'то',
        # 'ні', 'адже', 'он', 'тобто', 'уже', 'чи', 'аякже', 'це', 'тільки', 'ось', 'мов', 'немов']
        functors_pattern = re.compile(r"""(?ix)\b
        (?:в|на|зі?|за|до|по|у|біля|від|для|без|про|через|
        при|над|з[-−–]за|з[-−–]під|під|близько|вглиб|крізь|поза|
        проміж|і|й|що|так|хоча|коли|або|щоб|якщо|також|чи|проте|
        а|але|та|одначе|не|ж|же|навіть|би|б|лише|то|ні|адже|он|
        тобто|уже|аякже|це|тільки|ось|мов|немов)\b""")
        return bool(functors_pattern.match(self.get_letters()))

    def is_a_nnia_word(self) -> bool:
        if self.word_.normal_form.endswith("ння") or self.word_.normal_form.endswith("ття"):
            return True
        return False

    def is_a_sia_verb(self) -> bool:
        # VERB,*Refl*,impf infn
        if "Refl" in self.word_.tag:
            return True
        return False

    def is_a_no_to_verb(self) -> bool:
        # ('VERB,perf *Impe*')
        if "Impe" in self.word_.tag:
            return True
        return False

    def is_a_first_person_pronoun(self) -> bool:
        # я, ми не в оточенні дужок
        first_pronouns_pattern = re.compile(r"""(?x)(?:(?<=\s)|(?<=^))(?:я|ми)(?:(?=\s|[,.!?;:]|$)|(?=[)\]]))|
        (?<=[(\[])(?:я|ми)(?=\s|[,.!?;:])""")
        return bool(first_pronouns_pattern.match(self.get_letters()))

    def is_a_word(self) -> bool:
        return bool(re.search(
            r"(?i)[qazwsxedcrfvtgbyhnujmikolpąęłńóśźćżčďéěňřšťúůžйфяцічувскамепинртгоьшлбщдюзжхєїґёыэўъ\d]",
            self.word))


class Sentence(Analysis):
    def __init__(self, sentence: str, structure_per_sentence: dict):
        self.sentence = sentence
        self.sentence_structure = {"paragraph number": 0,
                                   "sentence number": 0,
                                   "number of words": 0,
                                   "average number of symbols per word": 0,
                                   "median number of symbols per word": 0,
                                   "number of subordinate clauses": 0,
                                   "dictionary of subordinates": {},
                                   "number of functors": 0,
                                   "dictionary of functors": {},
                                   "number of -nnia nouns": 0,
                                   "dictionary of -nnia nouns": {},
                                   "number of -sia verbs": 0,
                                   "dictionary of -sia verbs": {},
                                   "number of -no, -to verbs": 0,
                                   "dictionary of -no, -to verbs": {},
                                   "number of modal words": 0,
                                   "dictionary of modal words": {},
                                   "number of first pronouns": 0,
                                   "dictionary of first pronouns": {},
                                   "number of peoples' mentions": 0,
                                   "list of peoples' mentions": [],
                                   "sentence text": ''}
        self.structure_per_sentence = structure_per_sentence

        self.dictionary_of_subordinate_clauses_in_sentence = {}
        self.list_of_peoples_mentions_in_sentence = []
        self.number_of_functors_in_sentence = 0
        self.dict_of_functors_in_sentence = {}
        self.number_of_nnia_nouns_in_sentence = 0
        self.dict_of_nnia_nouns_in_sentence = {}
        self.dict_of_modal_words_in_sentence = {}
        self.number_of_sia_verbs_in_sentence = 0
        self.dict_of_sia_verbs_in_sentence = {}
        self.number_of_no_to_verbs_in_sentence = 0
        self.dict_of_no_to_verbs_in_sentence = {}
        self.number_of_first_pronouns_in_sentence = 0
        self.dict_of_first_pronouns_in_sentence = {}
        self.word_lengths = []

    def check_for_functors(self, word):
        if word.is_a_functor():
            self.number_of_functors_in_sentence += 1
            self.dict_of_functors_in_sentence = update(
                self.dict_of_functors_in_sentence, {word.get_letters().lower(): 1})

    def check_for_nnia_words(self, word):
        if word.is_a_nnia_word():
            self.number_of_nnia_nouns_in_sentence += 1
            self.dict_of_nnia_nouns_in_sentence = update(self.dict_of_nnia_nouns_in_sentence, {word.word_.normal_form: 1})

    def check_for_sia_verbs(self, word):
        if word.is_a_sia_verb():
            self.number_of_sia_verbs_in_sentence += 1
            self.dict_of_sia_verbs_in_sentence = update(self.dict_of_sia_verbs_in_sentence, {word.word_.normal_form: 1})

    def check_for_no_to_verbs(self, word):
        if word.is_a_no_to_verb():
            self.number_of_no_to_verbs_in_sentence += 1
            self.dict_of_no_to_verbs_in_sentence = update(self.dict_of_no_to_verbs_in_sentence, {word.word: 1})

    def check_for_first_pronouns(self, word):
        if word.is_a_first_person_pronoun():
            self.number_of_first_pronouns_in_sentence += 1
            self.dict_of_first_pronouns_in_sentence = update(self.dict_of_first_pronouns_in_sentence, {word.word: 1})

    def get_subordinate_clauses(self) -> int:
        sentence = self.sentence.lower()
        subordinates_pattern = re.compile(r"""(?x)(?:(?<=\W(?:проте|однак|потім|також|не\sте)\s)|(?<=\Wзате\s)|
        (?<=\W(?:але|там|або)\s)|(?<=\W(?:та|чи|то)\s)|(?<=\W[аій]\s)|(?<=,\s)|(?<=^))
        (?:щоби?|хто|як(?:що|би|ий|а|е)?|коби?|(?:на)?скільки|куди|
        (?:від)?коли|де|з?відк(?:и|іля)|бо|оскільки|позаяк|адже|(?:не)?(?:наче|мов)(?:би?(?:то)?)?|
        ніби(?:то)?|а?ніж|аби|навіщо|хоча?|(?:до|по|допо)ки|тільки|ледве|(?:не)?хай|скоро|аж|(?:(?:без|
        (?:по)?біля|у|в|від|од|для|до|і?з|коло|о?крім|між|ради|серед|задля|заради|(?:з[-−–])?
        (?:за|над|перед|під|поза|(?:пр?о)?м(?:іж|ежи)|понад|(?:по|на)[пс]еред|попід|позад)|щодо|близько|
        вглиб|вз?довж|(?:по)?(?:вище|нижче)|відносно|(?:до|на)вк(?:ола|іл|руги?)|замість|збоку|зверху?|
        ззаду|зсередини|кругом|(?:лі|пра)воруч(?:\sвід)?|мимо|на(?:в|су)?проти|назад|нап(?:еред(?:одні)?|рикінці)|
        недалеко|(?:непо|од|від)далік|обабіч|п?обі[кч]|опріч|о?круги?|осторонь|пізніше?|о?після|поблизу?|
        поверх|поз?довж|позад|поодаль|попере(?:ду|к)|пор(?:уч|яд)|посередині|(?:су)?проти|протягом|раніше?|
        спереду|стосовно|кінець|коштом|край|шляхом|ціною|внаслідок|в\s(?:ім'я|інтересах)|
        за\s(?:винятком|допомогою|посередництвом|рахунок|зразком)|з\s(?:боку|метою|нагоди|приводу)|
        (?:на|у)\sзнак|на\s(?:випадок|чолі|адресу|користь|честь|основі|зразок|кшталт|засадах|підставі|предмет)|
        під\sчас|по\sлінії|[ву]\s(?:бік|дусі|міру|напрям(?:і|ку)|плані|процесі|разі|результаті|розрізі|світлі|
        силу|справ(?:і|ах)|ході|умовах|сфері|межах|ролі|випадку|галузі|царині|районі|рамках)|під\sприводом|
        поза\s(?:сферою|межами)|через\sпосередництво|близько\sвід|виходячи\sз|відповідно\sдо|
        (?:(?:не\s)?(?:далеко|залежно)|збоку|на\sвідміну|(?:непо|од|від)далік|обіруч)\sвід|починаючи\s(?:від|з)|
        (?:стосовно|у\sнапрям(?:і|ку))(?:\sдо)?|на\sшляху\sдо|т(?:ого|ієї|ої|их))\s)?
        (?:кого|чого|(?:як|котр)(?:ого|ої|их)|ць?(?:ого|ієї|их)|чи(?:його|єї|їх))|
        (?:(?:вслід|всупереч|нав?здогін|навперейми|на(?:зу|в)стріч|наперекір|напереріз|завдяки|
        (?:на|у)\sпротивагу|у|в|на|об?|по|при|т(?:ому|ій|им))\s)?(?:кому|чому|
        (?:як|котр|ць?)(?:ому|ій|им)|чи(?:йому|їй|їм))|(?:(?:у|в|за|крізь|(?:пр?о)?(?:між|межи)|
        над?|об?|перед|під|по(?:вз|за|над|при)?|проз?|через|(?:(?:не)?зважаючи|у\sвідповідь|з\sогляду)\sна(?:\sте)?|
        так|дарма|хоч би|т(?:ому|ого|у|і(?:єї)?|их))\s)?(?:кого|що|(?:як|котр)(?:ого|ий|у|ої|е|і|их)|
        ць?(?:ого|ей|ю|і(?:єї)?|их)|чи(?:й(?:ого)?|ю|єї?|ї|їх))|(?:(?:(?:по|і)?з[іоа]?|(?:пр?о)?
        (?:між|межи|наді?|переді?)|піді?|(в?слід(?:ом)?|нав?здогін)\sза|(?:згідно|нарівні|на\sчолі|
        одночасно|паралельно|по(?:біч|рівняно|руч|ряд)|разом|[ув]\s(?:зв'язку|розріз|згоді|унісон|співдружності))
        \sі?з|т(?:им|ією|ою|ими))\s)?(?:ким|чим|(?:як|котр)(?:им|ою|ими)|ц(?:им|ією|ими)|чи(?:їм|єю|їми)))
        (?=\b)(?:\s(?:тільки|щоб?|як(?:що|би)?|коли|хоча|(?:до|по|допо)ки|б)(?=\b))?""")
        subordinates = [sub[0] for sub in subordinates_pattern.finditer(sentence)]
        number_of_subordinate_clauses = 0
        if len(subordinates) > 0:
            number_of_subordinate_clauses = len(subordinates)
            for subordinate in subordinates:
                self.dictionary_of_subordinate_clauses_in_sentence = update(
                    self.dictionary_of_subordinate_clauses_in_sentence, {subordinate: 1})
        return number_of_subordinate_clauses

    def get_number_people_mentioned(self) -> int:
        mentions_pattern = re.compile(r"""(?x)
(?<!“)(?:
(?:[А-ЯҐЇЄІ][а-яґіїє’']?\s*?\.\s*?(?:[-−–][А-ЯҐЇЄІ][а-яґіїє’']?\s*?\.\s*?)?){1,2}
[А-ЯҐЇЄІ][а-яґіїє’'А-ЯІЄЇҐ]+(?:[-−–][А-ЯҐЇЄІ][а-яґіїє’']+)?
|
(?:[A-Z][a-z]?\s*?\.\s*?(?:[-−–][A-Z][a-z]?\s*?\.\s*?)?){1,2}
[A-Z][a-z]+(?:[-−–][A-Z][a-z]+)?
|
[A-Z][a-z]+\s*?(?:[-−–][A-Z][a-z]+)?
(?:\s*?[A-Z][a-z]?\s*?\.(?:[-−–][A-Z][a-z]?\s*\.)?){1,2}
|
[А-ЯҐЇЄІ][а-яґіїє’']+\s*?(?:[-−–][А-ЯҐЇЄІ][а-яґіїє’']+)?
(?:\s*?[А-ЯҐЇЄІ][а-яґіїє’']?\s*?\.(?:[-−–][А-ЯҐЇЄІ][а-яґіїє’']?\s*\.)?){1,2}
|
(?<!^)(?<![-−–])(?<=\s)
(?:\s*?[А-ЯҐЇЄІ][а-яґіїє’']+(?:[-−–][А-ЯҐЇЄІ][а-яґіїє’']+)?){1,2}
|
(?<!^)(?<![-−–])(?<=\s)
(?:\s*?\b[A-Z][a-z]+(?:[-−–][A-Z][a-z]+\b)?){1,2}
)(?!”)""")
        findings = mentions_pattern.findall(self.sentence)
        if findings:
            for person in findings:
                if re.search(r"^(?:так|як|ні|не)$|\b(?:adj|copf|inf|pron|vf)\s", person.lower().strip()):
                    continue
                """If there is only last name, without initials or first name"""
                if " " not in person and "." not in person:
                    word = morph.parse(person)[0].normal_form
                    """If name ends with typical suffix"""
                    suffixes_pattern = re.compile(r"""(?x)
                    (?:[сз][оiе]н|[иі]н[гґ]а?|ер.?|ез|енс|
                    к[еі]н|л[еая]йн|швілі|ваті|шт[ае]йн.?|строн[гґ]|
                    ліц.?|манн?|офф?|мент|[гґ]іль|уа|ант|ей?ро|енас|
                    уліс|[ую]с|к[іау]с|а[гґ]о|[ая]к|[оі]в.?|[сцз]
                    ь?к[ои]й|е?нк.?|ан|ук|юк|єць|ч[аи]к|ич(?:на)?)$""")
                    if suffixes_pattern.search(word):
                        self.list_of_peoples_mentions_in_sentence.append(word.capitalize().strip('а'))
                else:
                    self.list_of_peoples_mentions_in_sentence.append(person)
        return len(self.list_of_peoples_mentions_in_sentence)

    def get_number_of_modal_words(self) -> int:
        modal_words_pattern = re.compile(r"""(?x)(?:на)?певно|(?:оче)?видно|либонь|можливо|мабуть|кажуть|мовляв|
        чую|бачу|чутно|як (?:кажуть|говорять|бачи(?:те|мо)|називається|на сьогодні|
        казав [А-ЯІЄЇҐ][-−–’'`А-ЯІЄЇҐа-яієїґ ]+)|певна річ|ясна річ|чого доброго|
        на (?:щастя|радість|диво|біду|.+?жаль|закінчення|(?:(?:нашу )?думку|
        (?:наш )?погляд)(?: [А-ЯІЄЇҐ][-−–’'`А-ЯІЄЇҐа-яієїґ ]+)?)|шкода|що не кажіть|виходить|зрештою|погодьтесь|
        дозвольте|бачите|уявіть собі|зверніть увагу|прошу(?: вас)?|крім того|нарешті|правда|головне|найголовніше|
        власне|сливе|буквально|так (?:би мовити|звані)|до речі|дійсно|зрозуміло|одна(?:к|че)|проте|(?:по)?між іншим|
        по-(?:перше|друге|третє|четверте|п'яте|моєму)|і останнє|наостано?ку?|по суті|от(ож|же)?|взагалі|значить|
        словом|зокрема|інакше кажучи|чуєте|уявіть|бачте|знаєте|повірте|справді|обов'язково|неодмінно|
        без ?сумнів(?:но|у)|звичайно|ймовірно|здається|може (?:бути)?|точно|вірно|воістину|ніде правди діти""")
        inserted_parts_pattern = re.compile(r"""(?x)(?:(?<=[-−–,])|(?<=^))
        (?: [-−–А-ЯІЄЇҐа-яієїґ]+){1,3}(?=[,.!]| [-−–]|$)""")
        inserted_parts = inserted_parts_pattern.findall(self.sentence)
        if inserted_parts:
            for part in inserted_parts:
                modal_word = modal_words_pattern.search(part.lower())
                if modal_word:
                    self.dict_of_modal_words_in_sentence = update(
                        self.dict_of_modal_words_in_sentence, {modal_word[0].strip(): 1})
        return sum(self.dict_of_modal_words_in_sentence.values())

    def parse_it(self, paragraph_counter=0, sentence_counter=1) -> dict:
        # print("START SENTENCE")
        # print(self.sentence)
        abbr_pattern = re.compile(r"""(?x)
        \b\d+(?:[-−–]\d+)?\b|\b[a-zа-яієїґ]+\.
        |\b[A-ZА-ЯІЄЇҐ][a-zа-яієїґ]?\.(?:[-−–][A-ZА-ЯІЄЇҐ][a-zа-яієїґ]?\.)?
        |\b[A-ZА-ЯІЄЇҐ]{2,}\b|\b[A-ZА-ЯІЄЇҐ]\b(?=,)""")
        sentence = self.sentence.split().copy()
        sentence[-1] = re.sub(r"(?<!\bр|\b[А-ЯІЄЇҐA-Z])(?<!\bст)(?<!ін)\.", "", sentence[-1])
        for word in sentence:
            the_word = Word(word)
            if the_word.is_a_word() and not abbr_pattern.search(word):
                self.check_for_nnia_words(the_word)
                self.check_for_functors(the_word)
                self.check_for_sia_verbs(the_word)
                self.check_for_no_to_verbs(the_word)
                self.check_for_first_pronouns(the_word)
                self.word_lengths.append(the_word.get_length())

        self.sentence_structure["paragraph number"] = paragraph_counter
        self.sentence_structure["sentence number"] = sentence_counter
        self.sentence_structure["number of words"] \
            = len([word for word in self.sentence.split() if Word(word).is_a_word()])
        self.sentence_structure["average number of symbols per word"] = get_average(self.word_lengths)
        self.sentence_structure["median number of symbols per word"] = get_median(self.word_lengths)
        self.sentence_structure["number of subordinate clauses"] = self.get_subordinate_clauses()
        self.sentence_structure["dictionary of subordinates"] = self.dictionary_of_subordinate_clauses_in_sentence
        self.sentence_structure["number of functors"] = self.number_of_functors_in_sentence
        self.sentence_structure["dictionary of functors"] = self.dict_of_functors_in_sentence
        self.sentence_structure["number of -nnia nouns"] = self.number_of_nnia_nouns_in_sentence
        self.sentence_structure["dictionary of -nnia nouns"] = self.dict_of_nnia_nouns_in_sentence
        self.sentence_structure["number of -sia verbs"] = self.number_of_sia_verbs_in_sentence
        self.sentence_structure["dictionary of -sia verbs"] = self.dict_of_sia_verbs_in_sentence
        self.sentence_structure["number of -no, -to verbs"] = self.number_of_no_to_verbs_in_sentence
        self.sentence_structure["dictionary of -no, -to verbs"] = self.dict_of_no_to_verbs_in_sentence
        self.sentence_structure["number of modal words"] = self.get_number_of_modal_words()
        self.sentence_structure["dictionary of modal words"] = self.dict_of_modal_words_in_sentence
        self.sentence_structure["number of first pronouns"] = self.number_of_first_pronouns_in_sentence
        self.sentence_structure["dictionary of first pronouns"] = self.dict_of_first_pronouns_in_sentence
        self.sentence_structure["number of peoples' mentions"] = self.get_number_people_mentioned()
        self.sentence_structure["list of peoples' mentions"] = self.list_of_peoples_mentions_in_sentence
        self.sentence_structure["sentence text"] = re.sub(r"\n", "\\\\n", self.sentence)
        self.structure_per_sentence[str(sentence_counter)] = self.sentence_structure
        return self.structure_per_sentence


class Paragraph(Analysis):
    def __init__(self, paragraph: list, structure_per_paragraph: dict):
        self.paragraph = paragraph
        self.paragraph_structure = {"paragraph number": 0,
                                    "number of words": 0,
                                    "number of sentences": 0,
                                    "average word length": 0,
                                    "median word length": 0,
                                    "average sentence length in words": 0,
                                    "median sentence length in words": 0,
                                    "number of subordinate clauses": 0,
                                    "average number of subordinate clauses per sentence": 0,
                                    "median number of subordinate clauses per sentence": 0,
                                    "dictionary of subordinates": {},
                                    "number of functors": 0,
                                    "average number of functors per sentence": 0,
                                    "median number of functors per sentence": 0,
                                    "dictionary of functors": 0,
                                    "number of -nnia nouns": 0,
                                    "average number of -nnia nouns per sentence": 0,
                                    "median number of -nnia nouns per sentence": 0,
                                    "number of -sia verbs": 0,
                                    "dictionary of -sia verbs": {},
                                    "average number of -sia verbs per sentence": 0,
                                    "median number of -sia verbs per sentence": 0,
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
                                    "dictionary of -nnia nouns": {},
                                    "number of peoples' mentions": 0,
                                    "list of peoples' mentions": [],
                                    "paragraph text": '',
                                    "structure per sentence": {}}
        self.structure_per_paragraph = structure_per_paragraph
        self.structure_per_sentence = {}

        self.paragraph_length_in_words = 0
        self.number_of_subordinate_clauses_in_paragraph = 0
        self.dictionary_of_subordinate_clauses_in_paragraph = {}
        self.number_of_functors_in_paragraph = 0
        self.number_of_peoples_mentions_in_paragraph = 0
        self.list_of_peoples_mentions_in_paragraph = []
        self.dict_of_functors_in_paragraph = {}
        self.number_of_nnia_nouns_in_paragraph = 0
        self.dict_of_nnia_nouns_in_paragraph = {}
        self.number_of_modal_words_in_paragraph = 0
        self.dict_of_modal_words_in_paragraph = {}
        self.number_of_first_pronouns_in_paragraph = 0
        self.dict_of_first_pronouns_in_paragraph = {}
        self.number_of_sia_verbs_in_paragraph = 0
        self.dict_of_sia_verbs_in_paragraph = {}
        self.number_of_no_to_verbs_in_paragraph = 0
        self.dict_of_no_to_verbs_in_paragraph = {}
        self.word_lengths = []
        self.list_of_list_elements = []

    def get_number_of_list_elements(self):
        list_pattern = re.compile(r"""(?x)(?:(?<=^)|(?<=\n))(?:
(?:[0-9]{1,2}\.){1,2}\s\[?[A-ZА-ЯІЄЇҐ]
|
[0-9]{1,2}\)(?=\s[^0-9/\\])
|
\s?\[
|
[•●*]\s+
|
[-−–]\s+
|
(?:[ІI]{1,3}|[ІI]?V(?:[ІI]{1,3})?|[ІI]?[XХ](?:[ІI]{1,3})?)\.\s+
)
[A-Za-zА-ЯІЄЇҐа-яієїґ’'` ]+?[\s\S]+?[.;]?\s?(?:[;:,ій]|та|чи|або|and|or)?\s?
(?:[(0-9]{1,2}\.?\s(?:Print|С.+|кн.+|kn.+|Вип.+|/.+|№.+|x.+)\.?)??
(?=\n|$)""")
        paragraph = " ".join(self.paragraph)
        self.list_of_list_elements = list_pattern.findall(paragraph)

    def parse_it(self, paragraph_counter=0, sentence_counter=0) -> dict:
        print("START PARAGRAPH")
        sentence_lengths_in_words = []
        number_of_subordinates = []
        number_of_functors = []
        number_of_nnia_nouns = []
        number_of_sia_verbs = []
        number_of_no_to_verbs = []
        number_of_modal_words = []
        number_of_first_pronouns = []

        for sentence in self.paragraph:
            sentence = sentence.strip(" \t\n")
            if sentence == '':
                continue
            sentence_id = str(sentence_counter + 1)

            the_sentence = Sentence(sentence, self.structure_per_sentence)
            self.structure_per_sentence = the_sentence.parse_it(paragraph_counter, int(sentence_id))

            subordinates = self.structure_per_sentence[sentence_id]["number of subordinate clauses"]
            number_of_subordinates.append(subordinates)
            if subordinates > 0:
                self.number_of_subordinate_clauses_in_paragraph += subordinates
                self.dictionary_of_subordinate_clauses_in_paragraph = update(
                    self.dictionary_of_subordinate_clauses_in_paragraph,
                    the_sentence.dictionary_of_subordinate_clauses_in_sentence)

            self.word_lengths.extend(the_sentence.word_lengths)
            self.paragraph_length_in_words += self.structure_per_sentence[sentence_id]["number of words"]
            sentence_lengths_in_words.append(self.structure_per_sentence[sentence_id]["number of words"])
            self.number_of_peoples_mentions_in_paragraph \
                += self.structure_per_sentence[sentence_id]["number of peoples' mentions"]
            self.list_of_peoples_mentions_in_paragraph.extend(the_sentence.list_of_peoples_mentions_in_sentence)

            parameters = ({0: "number of functors", 1: number_of_functors,
                           2: self.dict_of_functors_in_paragraph,
                           3: the_sentence.number_of_functors_in_sentence,
                           4: the_sentence.dict_of_functors_in_sentence},
                          {0: "number of -nnia nouns", 1: number_of_nnia_nouns,
                           2: self.dict_of_nnia_nouns_in_paragraph,
                           3: the_sentence.number_of_nnia_nouns_in_sentence,
                           4: the_sentence.dict_of_nnia_nouns_in_sentence},
                          {0: "number of -sia verbs", 1: number_of_sia_verbs,
                           2: self.dict_of_sia_verbs_in_paragraph,
                           3: the_sentence.number_of_sia_verbs_in_sentence,
                           4: the_sentence.dict_of_sia_verbs_in_sentence},
                          {0: "number of -no, -to verbs", 1: number_of_no_to_verbs,
                           2: self.dict_of_no_to_verbs_in_paragraph,
                           3: the_sentence.number_of_no_to_verbs_in_sentence,
                           4: the_sentence.dict_of_no_to_verbs_in_sentence},
                          {0: "number of modal words", 1: number_of_modal_words,
                           2: self.dict_of_modal_words_in_paragraph,
                           3: int(self.structure_per_sentence[sentence_id]["number of modal words"]),
                           4: the_sentence.dict_of_modal_words_in_sentence},
                          {0: "number of first pronouns", 1: number_of_first_pronouns,
                           2: self.dict_of_first_pronouns_in_paragraph,
                           3: the_sentence.number_of_first_pronouns_in_sentence,
                           4: the_sentence.dict_of_first_pronouns_in_sentence})
            for parameter_bag in parameters:
                parameter = self.structure_per_sentence[sentence_id][parameter_bag[0]]
                parameter_bag[1].append(parameter)
                if parameter > 0:
                    parameter_bag[2] = update(parameter_bag[2], parameter_bag[4])
                if parameter_bag[0] == "number of functors":
                    self.number_of_functors_in_paragraph += parameter_bag[3]
                elif parameter_bag[0] == "number of -nnia nouns":
                    self.number_of_nnia_nouns_in_paragraph += parameter_bag[3]
                elif parameter_bag[0] == "number of -sia verbs":
                    self.number_of_sia_verbs_in_paragraph += parameter_bag[3]
                elif parameter_bag[0] == "number of -no, -to verbs":
                    self.number_of_no_to_verbs_in_paragraph += parameter_bag[3]
                elif parameter_bag[0] == "number of modal words":
                    self.number_of_modal_words_in_paragraph += parameter_bag[3]
                elif parameter_bag[0] == "number of first pronouns":
                    self.number_of_first_pronouns_in_paragraph += parameter_bag[3]

            sentence_counter += 1

        self.get_number_of_list_elements()
        self.paragraph_structure["paragraph number"] = paragraph_counter
        self.paragraph_structure["number of words"] = self.paragraph_length_in_words
        self.paragraph_structure["number of sentences"] = len(self.paragraph)
        self.paragraph_structure["average word length"] = get_average(self.word_lengths)
        self.paragraph_structure["median word length"] = get_median(self.word_lengths)
        self.paragraph_structure["average sentence length in words"] = get_average(sentence_lengths_in_words)
        self.paragraph_structure["median sentence length in words"] = get_median(sentence_lengths_in_words)
        self.paragraph_structure["number of subordinate clauses"] = self.number_of_subordinate_clauses_in_paragraph
        self.paragraph_structure["average number of subordinate clauses per sentence"] \
            = get_average(number_of_subordinates)
        self.paragraph_structure["median number of subordinate clauses per sentence"] \
            = get_median(number_of_subordinates)
        self.paragraph_structure["dictionary of subordinates"] = self.dictionary_of_subordinate_clauses_in_paragraph
        self.paragraph_structure["number of functors"] = self.number_of_functors_in_paragraph
        self.paragraph_structure["average number of functors per sentence"] = get_average(number_of_functors)
        self.paragraph_structure["median number of functors per sentence"] = get_median(number_of_functors)
        self.paragraph_structure["dictionary of functors"] = self.dict_of_functors_in_paragraph
        self.paragraph_structure["number of -nnia nouns"] = self.number_of_nnia_nouns_in_paragraph
        self.paragraph_structure["dictionary of -nnia nouns"] = self.dict_of_nnia_nouns_in_paragraph
        self.paragraph_structure["average number of -nnia nouns per sentence"] = get_average(number_of_nnia_nouns)
        self.paragraph_structure["median number of -nnia nouns per sentence"] = get_median(number_of_nnia_nouns)
        self.paragraph_structure["number of -sia verbs"] = self.number_of_sia_verbs_in_paragraph
        self.paragraph_structure["dictionary of -sia verbs"] = self.dict_of_sia_verbs_in_paragraph
        self.paragraph_structure["average number of -sia verbs per sentence"] = get_average(number_of_sia_verbs)
        self.paragraph_structure["median number of -sia verbs per sentence"] = get_median(number_of_sia_verbs)
        self.paragraph_structure["number of -no, -to verbs"] = self.number_of_no_to_verbs_in_paragraph
        self.paragraph_structure["dictionary of -no, -to verbs"] = self.dict_of_no_to_verbs_in_paragraph
        self.paragraph_structure["average number of -no, -to verbs per sentence"] = get_average(number_of_no_to_verbs)
        self.paragraph_structure["median number of -no, -to verbs per sentence"] = get_median(number_of_no_to_verbs)
        self.paragraph_structure["number of modal words"] = self.number_of_modal_words_in_paragraph
        self.paragraph_structure["dictionary of modal words"] = self.dict_of_modal_words_in_paragraph
        self.paragraph_structure["average number of modal words per sentence"] = get_average(number_of_modal_words)
        self.paragraph_structure["median number of modal words per sentence"] = get_median(number_of_modal_words)
        self.paragraph_structure["number of first pronouns"] = self.number_of_first_pronouns_in_paragraph
        self.paragraph_structure["dictionary of first pronouns"] = self.dict_of_first_pronouns_in_paragraph
        self.paragraph_structure["average number of first pronouns per sentence"] = get_average(number_of_first_pronouns)
        self.paragraph_structure["median number of first pronouns per sentence"] = get_median(number_of_first_pronouns)
        self.paragraph_structure["number of peoples' mentions"] = self.number_of_peoples_mentions_in_paragraph
        self.paragraph_structure["list of peoples' mentions"] = self.list_of_peoples_mentions_in_paragraph
        self.paragraph_structure["paragraph text"] = re.sub(r"\n", "\\\\n", ' '.join(self.paragraph))
        self.paragraph_structure["structure per sentence"] = self.structure_per_sentence
        self.structure_per_paragraph[str(paragraph_counter)] = self.paragraph_structure
        return self.structure_per_paragraph


class Text(Analysis):
    def __init__(self, text: str, text_structure: dict, structure_per_paragraph: dict):
        self.text = re.split(r"""(?x)
        \t|(?<=\.)\n(?=(?:(?:\d{1,2}|
        [абвгґдеєжзиіїйкАБВГҐДЕЄЖЗИІЇЙК])[.)]
        |[-−–•●*])\s[А-ЯІЄЇҐ]|(?:[ІI]{1,3}|[ІI]?V(?:[ІI]{1,3})?|[ІI]?[XХ](?:[ІI]{1,3})?)\.\s)""", text)
        self.text_without_citations = " ".join(self.text)
        self.text_structure = text_structure
        self.text_structure["text"] = text.strip(' \n')
        self.structure_per_paragraph = structure_per_paragraph

        self.text_length_in_paragraphs = 0
        self.text_length_in_sentences = 0
        self.text_length_in_words = 0
        self.word_lengths = []

        self.number_of_drawings_in_text = 0
        self.number_of_tables_in_text = 0
        self.number_of_diagrams_in_text = 0
        self.number_of_graphs_in_text = 0
        self.number_of_examples = 0

        self.number_of_subordinate_clauses_in_text = 0
        self.dictionary_of_subordinate_clauses_in_text = {}
        self.number_of_functors_in_text = 0
        self.dict_of_functors_in_text = {}
        self.number_of_nnia_nouns_in_text = 0
        self.dict_of_nnia_nouns_in_text = {}
        self.number_of_modal_words_in_text = 0
        self.dict_of_modal_words_in_text = {}
        self.number_of_first_pronouns_in_text = 0
        self.dict_of_first_pronouns_in_text = {}
        self.number_of_sia_verbs_in_text = 0
        self.dict_of_sia_verbs_in_text = {}
        self.number_of_no_to_verbs_in_text = 0
        self.dict_of_no_to_verbs_in_text = {}

        self.number_of_words_cited_in_text = 0
        self.number_of_peoples_mentions_in_text = 0
        self.dictionary_of_punctuation_marks = {}
        self.list_of_peoples_mentions_in_text = []
        self.list_of_list_elements = []

    def get_number_of_lists(self) -> int:
        ordered_list_patterns = {re.compile(r"(?:[0-9]{1,2}\.){1,2}\s.+"): [],
                                 re.compile(r"[0-9]{1,2}\).+"): [],
                                 re.compile(r"[абвгґдеєзжиіїйклмн]\)\s.+"): [],
                                 re.compile(r"(?:[ІI]{1,3}|[ІI]?V(?:[ІI]{1,3})?|[ІI]?[XХ](?:[ІI]{1,3})?)\.\s+.+"): []}
        unordered_list_patterns = (re.compile(r"[-−–]\s.+"),
                                   re.compile(r"•\s.+"),
                                   re.compile(r"●\s.+"),
                                   re.compile(r"\*\s.+"),
                                   re.compile(r"\s.+"),
                                   re.compile(r"\s?\[.+"))
        number_of_unordered_lists = 0
        number_of_ordered_lists = 0
        list_counter = 0
        match = False
        # [print(el) for el in self.list_of_list_elements]
        while list_counter < len(self.list_of_list_elements):
            for ordered_pattern in ordered_list_patterns:
                if ordered_pattern.match(self.list_of_list_elements[list_counter]):
                    ordered_list_patterns[ordered_pattern].append(self.list_of_list_elements[list_counter])
                else:
                    for unordered_pattern in unordered_list_patterns:
                        if unordered_pattern.match(self.list_of_list_elements[list_counter]):
                            match = True
                            break
            if match or self.list_of_list_elements[list_counter - 1] == self.list_of_list_elements[-1]:
                match = False
                number_of_unordered_lists += 1
            list_counter += 1
        number_of_seconds = 0
        for lists in ordered_list_patterns.values():
            if lists:
                for lst in lists:
                    if lst.startswith("1") or lst.startswith("a") or lst.startswith("а") \
                            or lst.startswith("I.") or lst.startswith("І."):
                        number_of_ordered_lists += 1
                    if lst.startswith("2") or lst.startswith("б") or re.match(r"[IІ]{2}\.", lst):
                        number_of_seconds += 1
                if number_of_ordered_lists == 0:
                    number_of_ordered_lists = len(lists)
                if number_of_seconds > number_of_ordered_lists:
                    number_of_ordered_lists = number_of_seconds
        return number_of_ordered_lists + number_of_unordered_lists

    def how_many_words_are_cited(self) -> float:
        text = self.text_without_citations
        # print(text)
        citations = []
        citations_lengths = []
        first_citation_pattern = re.compile(r"""(?x)(?:
    “[^“]+?[”ˮ]
    |
    «[^«]+?»
    |
    (?<!..\(див|.\(див\.|.\(напр|\(напр\.)(?<=..:\s|\d\),\s)\d[^«“]+?
    )
    \s?[(\[](?:див\.?:\s?)?
    (?:
    (?:[А-ЯІЄЇҐA-Z]\.[-−–]?){1,2}.+
    |
    (?:(?:['’А-ЯІЄЇҐA-Z][’'а-яієїґa-z]+[-−–]?)+,?\s?)+(?:(?::\s?)?(?:\d+[-−–,]?\s?)+)?
    |
    \d{1,2}(?:,\ [cс]\.\ \d+)?
    )
    [])]
    |
    (?<!..\(див|.\(див\.|.\(напр|\(напр\.)(?<=..:\s|\d\),\s)\D[^«“]+?[^)]
    \s[(\[][А-ЯІЄЇҐA-Z]+,\ \d+[])]""")
        second_citation_pattern = re.compile(r"""(?x)(?:
    «[^«]+?»[ \t\S]?
    |
    “[^“]+?[”ˮ][ \t\S]?
    |
    (?<=(?<!..\(див|.\(див\.|.\(напр|\(напр\.):\s)\D.+?[^)])
    (?=\s.*(?:[(\[]див\.?:\s?)?[(\[]
    (?:(?:[А-ЯІЄЇҐA-Z]\.[-−–]?){1,2}.+
    |
    (?:(?:['А-ЯІЄЇҐA-Z]['а-яієїґa-z]+[-−–]?)+,?\s?)+(?:(?::\s?)?(?:\d+[-−–,]?\s?)+)?
    |
    \d{1,2}(?:,\ [cс]\.\ \d+)?
    )
    [])])""")
        clear_citation_pattern = re.compile(r"""(?x)
    (?:«[^»]+?(?:\s[^»]+?)+»
    |
    “[^”ˮ]+?(?:\s[^”ˮ]+?)+[”ˮ])[^$]
    |
    .+?
    (?=\s[(\[][А-ЯІЄЇҐA-Z]+,\ \d+[])])""")
        final_citation_pattern = re.compile(r"^.+?(?=\s[(\[][А-ЯІЄЇҐA-Z\d]+(?:[a-zа-яієїґ]+)? ?[,;:.] \d+[])])")

        if not first_citation_pattern.search(text):
            precitations = second_citation_pattern.findall(text)
        else:
            precitations = first_citation_pattern.findall(text)
        # print("START of CITATIONS")
        # [print(precitation) for precitation in precitations]
        for precitation in precitations:
            self.text_without_citations = self.text_without_citations.replace(precitation, " ", 1)
            if not clear_citation_pattern.search(precitation):
                citations.extend(final_citation_pattern.findall(precitation))
                continue
            # print("CITE")

            citations.extend(clear_citation_pattern.findall(precitation))

        for citation in citations:
            citation = [word for word in citation.split() if Word(word).is_a_word()]
            citations_lengths.append(len(citation))

        number_of_words_cited = sum(citations_lengths)
        return number_of_words_cited

    def get_number_of_punctuation_marks(self) -> int:
        punctuation_pattern = re.compile(r"""(?x)
        [,!?…]|(?<!\s[A-ZА-ЯІЄЇҐ\d])\.|
        [:;](?![^(\[\n]*?[])])|(?<!\S)[-−–](?!\S)|
        \((?=[^(]+?\))|\[(?=[^\[]+?])""")
        punctuation_marks = punctuation_pattern.findall(self.text_without_citations)
        if not punctuation_marks:
            return 0

        for punctuation_mark in punctuation_marks:
            if punctuation_mark == "(":
                punctuation_mark = "()"
            if punctuation_mark == "[":
                punctuation_mark = "[]"
            if punctuation_mark == "–" or punctuation_mark == "−":
                punctuation_mark = "-"

            if punctuation_mark in self.dictionary_of_punctuation_marks:
                self.dictionary_of_punctuation_marks[punctuation_mark] += 1
            else:
                self.dictionary_of_punctuation_marks[punctuation_mark] = 1
        return len(punctuation_marks)

    def parse_it(self, paragraph_counter=0, sentence_counter=0) -> tuple:
        print("START TEXT")
        paragraph_lengths_in_sentences = []
        paragraph_sentence_lengths_in_words = []
        average_numbers_of_subordinates_in_paragraph = []
        paragraph_numbers_of_functors = []
        paragraph_numbers_of_nnia_nouns = []
        paragraph_numbers_of_modal_words = []
        paragraph_numbers_of_first_pronouns = []
        paragraph_numbers_of_sia_verbs = []
        paragraph_numbers_of_no_to_verbs = []

        self.text_length_in_paragraphs = len(self.text)

        for paragraph in self.text:
            paragraph = paragraph.strip(' \t\n')

            if paragraph == '':
                self.text_length_in_paragraphs -= 1
                continue

            drawing_pattern = re.compile(r"(?:Рис|Мал|Фото)(?:[ \t]*\.|у?ю?нок)[ \t]*[0-9]{1,2}[ \t]*\.?")
            if drawing_pattern.match(paragraph):
                self.number_of_drawings_in_text += 1
                self.text_length_in_paragraphs -= 1
                continue

            table_pattern = re.compile(r"Табл?(?:[ \t]*\.|л?иця)[ \t]*[0-9]{1,2}[ \t]*\.?")
            if table_pattern.match(paragraph):
                self.number_of_tables_in_text += 1
                self.text_length_in_paragraphs -= 1
                continue

            diagram_pattern = re.compile(r"(?:Діаг|Ментальна карта)(?:[ \t]*\.|рама)[ \t]*[0-9]{1,2}[ \t]*\.?")
            if diagram_pattern.match(paragraph):
                self.number_of_diagrams_in_text += 1
                self.text_length_in_paragraphs -= 1
                continue

            graph_pattern = re.compile(r"Графік[ \t]*[0-9]{1,2}[ \t]*\.?")
            if graph_pattern.match(paragraph):
                self.number_of_graphs_in_text += 1
                self.text_length_in_paragraphs -= 1
                continue

            example_pattern = re.compile(r"Приклад\s?\d{1,2}\.?\s.+")
            if example_pattern.match(paragraph):
                self.number_of_examples += 1
                self.text_length_in_paragraphs -= 1
                # print("EXAMPLE")
                continue

            sentence_pattern = re.compile(r"""(?x)(?<=(?<!(?:^|\b)[А-ЯЄїІҐA-Z]|[0-9]|
                                            \bр)[.?!])[ \t]+(?=[«“\"]?[А-ЯІЇЄҐA-Z\[](?![)\]]))""")
            additional_pattern = re.compile(r"[А-Яа-яіІїЇєЄґҐA-Za-z ]+[)\]]")
            sentences_of_paragraph = sentence_pattern.split(paragraph)
            for element in range(len(sentences_of_paragraph)):
                if additional_pattern.match(sentences_of_paragraph[element]):
                    ' '.join(sentences_of_paragraph[element - 1: element + 1])

            the_paragraph = Paragraph(sentences_of_paragraph, self.structure_per_paragraph)
            self.structure_per_paragraph = the_paragraph.parse_it(paragraph_counter+1)

            self.list_of_list_elements.extend(the_paragraph.list_of_list_elements)
            self.number_of_functors_in_text += the_paragraph.number_of_functors_in_paragraph
            self.dict_of_functors_in_text = update(
                self.dict_of_functors_in_text, the_paragraph.dict_of_functors_in_paragraph)
            self.number_of_nnia_nouns_in_text += the_paragraph.number_of_nnia_nouns_in_paragraph
            self.dict_of_nnia_nouns_in_text = update(
                self.dict_of_nnia_nouns_in_text, the_paragraph.dict_of_nnia_nouns_in_paragraph)
            self.number_of_first_pronouns_in_text += the_paragraph.number_of_first_pronouns_in_paragraph
            self.dict_of_first_pronouns_in_text = update(
                self.dict_of_first_pronouns_in_text, the_paragraph.dict_of_first_pronouns_in_paragraph)
            self.number_of_modal_words_in_text += the_paragraph.number_of_modal_words_in_paragraph
            self.dict_of_modal_words_in_text = update(
                self.dict_of_modal_words_in_text, the_paragraph.dict_of_modal_words_in_paragraph)
            self.number_of_no_to_verbs_in_text += the_paragraph.number_of_no_to_verbs_in_paragraph
            self.dict_of_no_to_verbs_in_text = update(
                self.dict_of_no_to_verbs_in_text, the_paragraph.dict_of_no_to_verbs_in_paragraph)
            self.number_of_sia_verbs_in_text += the_paragraph.number_of_sia_verbs_in_paragraph
            self.dict_of_sia_verbs_in_text = update(
                self.dict_of_sia_verbs_in_text, the_paragraph.dict_of_sia_verbs_in_paragraph)
            self.number_of_peoples_mentions_in_text += the_paragraph.number_of_peoples_mentions_in_paragraph
            self.list_of_peoples_mentions_in_text.extend(the_paragraph.list_of_peoples_mentions_in_paragraph)

            paragraph_numbers_of_functors.append(the_paragraph.number_of_functors_in_paragraph)
            paragraph_numbers_of_nnia_nouns.append(the_paragraph.number_of_nnia_nouns_in_paragraph)
            paragraph_numbers_of_modal_words.append(the_paragraph.number_of_modal_words_in_paragraph)
            paragraph_numbers_of_first_pronouns.append(the_paragraph.number_of_first_pronouns_in_paragraph)
            paragraph_numbers_of_sia_verbs.append(the_paragraph.number_of_sia_verbs_in_paragraph)
            paragraph_numbers_of_no_to_verbs.append(the_paragraph.number_of_no_to_verbs_in_paragraph)

            self.text_length_in_sentences += self.structure_per_paragraph[
                str(paragraph_counter+1)]["number of sentences"]
            self.text_length_in_words += the_paragraph.paragraph_length_in_words
            paragraph_lengths_in_sentences.append(
                self.structure_per_paragraph[str(paragraph_counter+1)]["number of sentences"])
            paragraph_sentence_lengths_in_words.append(
                self.structure_per_paragraph[str(paragraph_counter+1)]["average sentence length in words"])
            average_numbers_of_subordinates_in_paragraph.append(
                self.structure_per_paragraph[str(paragraph_counter+1)][
                    "average number of subordinate clauses per sentence"])
            self.dictionary_of_subordinate_clauses_in_text = update(self.dictionary_of_subordinate_clauses_in_text,
                     the_paragraph.dictionary_of_subordinate_clauses_in_paragraph)
            self.number_of_subordinate_clauses_in_text += the_paragraph.number_of_subordinate_clauses_in_paragraph
            paragraph_counter += 1
            self.word_lengths.extend(the_paragraph.word_lengths)

        sentence_lengths_in_words = []
        numbers_of_subordinates_per_sentence = []
        numbers_of_functors_per_sentence = []
        numbers_of_nnia_nouns_per_sentence = []
        if self.structure_per_paragraph and len(self.structure_per_paragraph[str(paragraph_counter)]["structure per sentence"].values()) > 0:
            for sentence in self.structure_per_paragraph[str(paragraph_counter)]["structure per sentence"].values():
                sentence_lengths_in_words.append(sentence["number of words"])
                numbers_of_subordinates_per_sentence.append(sentence["number of subordinate clauses"])
                numbers_of_functors_per_sentence.append(sentence["number of functors"])
                numbers_of_nnia_nouns_per_sentence.append(sentence["number of -nnia nouns"])

        self.text_structure["number of words"] = self.text_length_in_words
        self.text_structure["number of sentences"] = self.text_length_in_sentences
        self.text_structure["number of paragraphs"] = self.text_length_in_paragraphs
        self.text_structure["number of drawings"] = self.number_of_drawings_in_text
        self.text_structure["number of tables"] = self.number_of_tables_in_text
        self.text_structure["number of diagrams"] = self.number_of_diagrams_in_text
        self.text_structure["number of graphs"] = self.number_of_graphs_in_text
        self.text_structure["number of examples"] = self.number_of_examples
        print("END PARAGRAPHs")
        self.text_structure["number of lists"] = self.get_number_of_lists()
        self.text_structure["average word length"] = get_average(self.word_lengths)
        self.text_structure["median word length"] = get_median(self.word_lengths)
        self.text_structure["average sentence length in words"] = get_average(sentence_lengths_in_words)
        self.text_structure["median sentence length in words"] = get_median(sentence_lengths_in_words)
        self.text_structure["average paragraph length in sentences"] = get_average(paragraph_lengths_in_sentences)
        self.text_structure["median paragraph length in sentences"] = get_median(paragraph_lengths_in_sentences)
        self.text_structure["number of subordinate clauses"] = self.number_of_subordinate_clauses_in_text
        self.text_structure["average number of subordinate clauses per sentence"] \
            = get_average(average_numbers_of_subordinates_in_paragraph)
        self.text_structure["median number of subordinate clauses per sentence"] \
            = get_median(numbers_of_subordinates_per_sentence)
        self.text_structure["dictionary of subordinates"] = self.dictionary_of_subordinate_clauses_in_text
        self.text_structure["number of functors"] = self.number_of_functors_in_text
        self.text_structure["average number of functors per sentence"] \
            = get_average(numbers_of_functors_per_sentence)
        self.text_structure["median number of functors per sentence"] \
            = get_median(numbers_of_functors_per_sentence)
        self.text_structure["dictionary of functors"] = self.dict_of_functors_in_text
        self.text_structure["number of -nnia nouns"] = self.number_of_nnia_nouns_in_text
        self.text_structure["average number of -nnia nouns"] = get_average(numbers_of_nnia_nouns_per_sentence)
        self.text_structure["median number of -nnia nouns per sentence"] \
            = get_median(numbers_of_nnia_nouns_per_sentence)
        self.text_structure["dictionary of -nnia nouns"] = self.dict_of_nnia_nouns_in_text
        self.text_structure["number of -sia verbs"] = self.number_of_sia_verbs_in_text
        self.text_structure["dictionary of -sia verbs"] = self.dict_of_sia_verbs_in_text
        self.text_structure["average number of -sia verbs per sentence"] = get_average(paragraph_numbers_of_sia_verbs)
        self.text_structure["median number of -sia verbs per sentence"] = get_median(paragraph_numbers_of_sia_verbs)
        self.text_structure["number of -no, -to verbs"] = self.number_of_no_to_verbs_in_text
        self.text_structure["dictionary of -no, -to verbs"] = self.dict_of_no_to_verbs_in_text
        self.text_structure["average number of -no, -to verbs per sentence"] = get_average(paragraph_numbers_of_no_to_verbs)
        self.text_structure["median number of -no, -to verbs per sentence"] = get_median(paragraph_numbers_of_no_to_verbs)
        self.text_structure["number of modal words"] = self.number_of_modal_words_in_text
        self.text_structure["dictionary of modal words"] = self.dict_of_modal_words_in_text
        self.text_structure["average number of modal words per sentence"] = get_average(paragraph_numbers_of_modal_words)
        self.text_structure["median number of modal words per sentence"] = get_median(paragraph_numbers_of_modal_words)
        self.text_structure["number of first pronouns"] = self.number_of_first_pronouns_in_text
        self.text_structure["dictionary of first pronouns"] = self.dict_of_first_pronouns_in_text
        self.text_structure["average number of first pronouns per sentence"] = get_average(
            paragraph_numbers_of_first_pronouns)
        self.text_structure["median number of first pronouns per sentence"] = get_median(paragraph_numbers_of_first_pronouns)
        self.text_structure["number of peoples' mentions"] = self.number_of_peoples_mentions_in_text
        self.text_structure["list of peoples' mentions"] = self.list_of_peoples_mentions_in_text

        self.text_structure["number of cited words"] = self.how_many_words_are_cited()
        self.text_structure["number of punctuation marks"] = self.get_number_of_punctuation_marks()
        try:
            self.text_structure["average number of punctuation marks per sentence"] = \
                self.get_number_of_punctuation_marks() / self.text_length_in_sentences
        except ZeroDivisionError:
            self.text_structure["average number of punctuation marks per sentence"] = \
                self.get_number_of_punctuation_marks() / 1
        self.text_structure["dictionary of punctuation marks"] = self.dictionary_of_punctuation_marks
        return self.text_structure, self.structure_per_paragraph
