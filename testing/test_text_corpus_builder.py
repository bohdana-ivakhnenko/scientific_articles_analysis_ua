import unittest
import json


class TestTextStructure(unittest.TestCase):
    def setUp(self):
        with open(
            "C:\\Users\\Bohdanka\\PycharmProjects\\Навчання\\2 курс\\Курсова\\Корпус наукових статей\\testing materials\\Science_Art_Corp.json",
                "r", encoding="utf-8") as file:
            self.compmade_text = json.load(file)

        with open(
            "C:\\Users\\Bohdanka\\PycharmProjects\\Навчання\\2 курс\\Курсова\\Корпус наукових статей\\testing materials\\Cherevchenko_I.json",
                "r", encoding="utf-8") as file:
            self.handmade_text = json.load(file)

    def test_num_of_words(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["number of words"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["number of words"])

    def test_num_of_sentences(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["number of sentences"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["number of sentences"])

    def test_num_of_paragraphs(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["number of paragraphs"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["number of paragraphs"])

    def test_num_of_drawings(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["number of drawings"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["number of drawings"])

    def test_num_of_tables(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["number of tables"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["number of tables"])

    def test_num_of_diagrams(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["number of diagrams"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["number of diagrams"])

    def test_num_of_graphs(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["number of graphs"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["number of graphs"])

    def test_num_of_lists(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["number of lists"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["number of lists"])

    def test_ave_word_length(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["average word length"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["average word length"])

    def test_med_word_length(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["median word length"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["median word length"])

    def test_ave_sentence_length(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["average sentence length in words"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["average sentence length in words"])

    def test_med_sentence_length(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["median sentence length in words"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["median sentence length in words"])

    def test_ave_paragraph_length(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["average paragraph length in sentences"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["average paragraph length in sentences"])

    def test_med_paragraph_length(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["median paragraph length in sentences"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["median paragraph length in sentences"])

    def test_num_of_subordinates(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["number of subordinate clauses"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["number of subordinate clauses"])

    def test_ave_num_of_subordinates(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["average number of subordinate clauses per sentence"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["average number of subordinate clauses per sentence"])

    def test_med_num_of_subordinates(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["median number of subordinate clauses per sentence"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["median number of subordinate clauses per sentence"])

    def test_dict_of_subordinates(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["dictionary of subordinates"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["dictionary of subordinates"])

    def test_num_of_functors(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["number of functors"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["number of functors"])

    def test_ave_num_of_functors(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["average number of functors per sentence"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["average number of functors per sentence"])

    def test_med_num_of_functors(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["median number of functors per sentence"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["median number of functors per sentence"])

    def test_dict_of_functors(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["dictionary of functors"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["dictionary of functors"])

    def test_num_of_nnia_nouns(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["number of -nnia nouns"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["number of -nnia nouns"])

    def test_ave_num_of_nnia_nouns(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["average number of -nnia nouns per sentence"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["average number of -nnia nouns"])

    def test_med_num_of_nnia_nouns(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["median number of -nnia nouns per sentence"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["median number of -nnia nouns per sentence"])

    def test_dict_of_nnia_nouns(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["dictionary of -nnia nouns"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["dictionary of -nnia nouns"])

    def test_num_of_cited_words(self):
        self.assertTrue(self.compmade_text["corpus"][0]["statistics"]["text structure"]["number of cited words"]-
                        self.handmade_text["corpus"][0]["statistics"]["text structure"]["number of cited words"] < 10)

    def test_dict_of_mentions(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["number of peoples' mentions"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["number of peoples' mentions"])

    def test_list_of_mentions(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["list of peoples' mentions"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["list of peoples' mentions"])

    def test_num_of_punctuation_marks(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["number of punctuation marks"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["number of punctuation marks"])

    def test_dict_of_punctuation_marks(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["dictionary of punctuation marks"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["dictionary of punctuation marks"])

    def test_text(self):
        self.assertEqual(self.handmade_text["corpus"][0]["statistics"]["text structure"]["text"],
                         self.compmade_text["corpus"][0]["statistics"]["text structure"]["text"])

    def tearDown(self):
        del self.compmade_text
        del self.handmade_text


if __name__ == "__main__":
    unittest.main()
