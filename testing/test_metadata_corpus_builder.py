# !/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import json


class TestMetadata(unittest.TestCase):
    def setUp(self):
        with open("C:\\Users\\Bohdanka\\PycharmProjects\\Навчання\\2 курс\\Курсова\\Корпус наукових статей\\testing\\testing materials\\Science_Art_Corp.json", 'r', encoding='utf-8') as file:
            self.compmade_text = json.load(file)

        with open("C:\\Users\\Lenovo\\PycharmProjects\\ScientificArticles\\Тестові матеріали\\Cherevchenko_I.json", 'r', encoding='utf-8') as file:
            self.handmade_text = json.load(file)

        with open("C:\\Users\\Lenovo\\PycharmProjects\\ScientificArticles\\Тестові матеріали\\Corpus_from_empty_file.json", 'r', encoding='utf-8') as file:
            self.empty_text = json.load(file)

    def test_empty_file(self):
        metadata = {"journal": '', "journal type": '', "author": [], "institution": '', "title": [], "doi": '', "year": '', "udc": '', "keywords": {"in Ukrainian": [], "in English": [], "in russian": []}, "annotation": {"in Ukrainian": '', "in English": '', "in russian": ''}, "abbreviations": {"in Ukrainian": [], "in English": []}, "sources": {"in Ukrainian": [], "in English": []}, "references": {"in Ukrainian": [], "in English": []}}
        self.assertEqual(metadata, self.empty_text['corpus'][0]['metadata'])

    def test_journal(self):
        self.assertEqual(self.handmade_text['corpus'][0]['metadata']['journal'], self.compmade_text['corpus'][0]['metadata']['journal'])

    def test_journal_type(self):
        self.assertEqual(self.handmade_text['corpus'][0]['metadata']['journal type'], self.compmade_text['corpus'][0]['metadata']['journal type'])

    def test_author(self):
        self.assertEqual(self.handmade_text['corpus'][0]['metadata']['author'], self.compmade_text['corpus'][0]['metadata']['author'])

    def test_institution(self):
        self.assertEqual(self.handmade_text['corpus'][0]['metadata']['institution'], self.compmade_text['corpus'][0]['metadata']['institution'])

    def test_title(self):
        self.assertEqual(self.handmade_text['corpus'][0]['metadata']['title'], self.compmade_text['corpus'][0]['metadata']['title'])

    def test_doi(self):
        self.assertEqual(self.handmade_text['corpus'][0]['metadata']['doi'], self.compmade_text['corpus'][0]['metadata']['doi'])

    def test_year(self):
        self.assertEqual(self.handmade_text['corpus'][0]['metadata']['year'], self.compmade_text['corpus'][0]['metadata']['year'])

    def test_udc(self):
        self.assertEqual(self.handmade_text['corpus'][0]['metadata']['udc'], self.compmade_text['corpus'][0]['metadata']['udc'])

    def test_keywords_ukr(self):
        self.assertEqual(self.handmade_text['corpus'][0]['metadata']['keywords']['in Ukrainian'], self.compmade_text['corpus'][0]['metadata']['keywords']['in Ukrainian'])

    def test_keywords_eng(self):
        self.assertEqual(self.handmade_text['corpus'][0]['metadata']['keywords']['in English'], self.compmade_text['corpus'][0]['metadata']['keywords']['in English'])

    def test_keywords_ru(self):
        self.assertEqual(self.handmade_text['corpus'][0]['metadata']['keywords']['in russian'], self.compmade_text['corpus'][0]['metadata']['keywords']['in russian'])

    def test_annotation_ukr(self):
        self.assertEqual(self.handmade_text['corpus'][0]['metadata']['annotation']['in Ukrainian'], self.compmade_text['corpus'][0]['metadata']['annotation']['in Ukrainian'])

    def test_annotation_eng(self):
        self.assertEqual(self.handmade_text['corpus'][0]['metadata']['annotation']['in English'], self.compmade_text['corpus'][0]['metadata']['annotation']['in English'])

    def test_annotation_ru(self):
        self.assertEqual(self.handmade_text['corpus'][0]['metadata']['annotation']['in russian'], self.compmade_text['corpus'][0]['metadata']['annotation']['in russian'])

    def test_abbreviations_ukr(self):
        self.assertEqual(self.handmade_text['corpus'][0]['metadata']['abbreviations']['in Ukrainian'], self.compmade_text['corpus'][0]['metadata']['abbreviations']['in Ukrainian'])

    def test_abbreviations_eng(self):
        self.assertEqual(self.handmade_text['corpus'][0]['metadata']['abbreviations']['in English'], self.compmade_text['corpus'][0]['metadata']['abbreviations']['in English'])

    def test_sources_ukr(self):
        self.assertEqual(self.handmade_text['corpus'][0]['metadata']['sources']['in Ukrainian'], self.compmade_text['corpus'][0]['metadata']['sources']['in Ukrainian'])

    def test_sources_eng(self):
        self.assertEqual(self.handmade_text['corpus'][0]['metadata']['sources']['in English'], self.compmade_text['corpus'][0]['metadata']['sources']['in English'])

    def test_references_ukr(self):
        self.assertEqual(self.handmade_text['corpus'][0]['metadata']['references']['in Ukrainian'], self.compmade_text['corpus'][0]['metadata']['references']['in Ukrainian'])

    def test_references_eng(self):
        self.assertEqual(self.handmade_text['corpus'][0]['metadata']['references']['in English'], self.compmade_text['corpus'][0]['metadata']['references']['in English'])

    def tearDown(self):
        del self.compmade_text
        del self.handmade_text


if __name__ == "__main__":
    unittest.main()
