import unittest
import json


class TestParagraphStructure(unittest.TestCase):
    def setUp(self):
        compmade_file_path = "C:\\Users\\Bohdanka\\PycharmProjects\\Навчання\\2 курс\\Курсова\\Корпус наукових статей\\testing materials\\Science_Art_Corp.json"
        with open(compmade_file_path, 'r', encoding='utf-8') as file:
            self.compmade_text = json.load(file)

        handmade_file_path = "C:\\Users\\Bohdanka\\PycharmProjects\\Навчання\\2 курс\\Курсова\\Корпус наукових статей\\testing materials\\Cherevchenko_I.json"
        with open(handmade_file_path, 'r', encoding='utf-8') as file:
            self.handmade_text = json.load(file)

    def test_paragraph_number(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["paragraph number"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["paragraph number"])

    def test_num_of_words(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["number of words"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["number of words"])

    def test_num_of_sentences(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["number of sentences"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["number of sentences"])

    def test_ave_word_length(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["average word length"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["average word length"])

    def test_med_word_length(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["median word length"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["median word length"])

    def test_ave_sentence_length(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["average sentence length in words"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["average sentence length in words"])

    def test_med_sentence_length(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["median sentence length in words"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["median sentence length in words"])

    def test_num_of_subordinates(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["number of subordinate clauses"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["number of subordinate clauses"])

    def test_ave_num_of_subordinates(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["average number of subordinate clauses per sentence"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["average number of subordinate clauses per sentence"])

    def test_med_num_of_subordinates(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["median number of subordinate clauses per sentence"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["median number of subordinate clauses per sentence"])

    def test_dict_of_subordinates(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["dictionary of subordinates"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["dictionary of subordinates"])

    def test_num_of_functors(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["number of functors"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["number of functors"])

    def test_ave_num_of_functors(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["average number of functors per sentence"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["average number of functors per sentence"])

    def test_med_num_of_functors(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["median number of functors per sentence"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["median number of functors per sentence"])

    def test_dict_of_functors(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["dictionary of functors"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["dictionary of functors"])

    def test_num_of_nnia_nouns(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["number of -nnia nouns"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["number of -nnia nouns"])

    def test_ave_num_of_nnia_nouns(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["average number of -nnia nouns per sentence"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["average number of -nnia nouns per sentence"])

    def test_med_num_of_nnia_nouns(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["median number of -nnia nouns per sentence"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["median number of -nnia nouns per sentence"])

    def test_dict_of_nnia_nouns(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["dictionary of -nnia nouns"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["dictionary of -nnia nouns"])

    def test_num_of_words_cited(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["number of words cited"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["number of words cited"])

    def test_num_of_people_mentions(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["number of peoples' mentions"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["number of peoples' mentions"])

    def test_list_of_people_mentions(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["list of peoples' mentions"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["list of peoples' mentions"])

    def test_paragraph_text(self):
        self.assertEqual(self.handmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["paragraph text"],
                         self.compmade_text['corpus'][0]['statistics']['structure per paragraph'][10]["paragraph text"])

    def tearDown(self):
        del self.compmade_text
        del self.handmade_text


if __name__ == '__main__':
    unittest.main()
