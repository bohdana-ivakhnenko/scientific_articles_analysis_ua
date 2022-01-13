# scientific_articles_analysis_ua
A course paper project dedicated to automatically detect parts of low readability text in scientific articles (for the Ukrainian language).

## Description
### Purpose
To measure the readability of scientific articles in the Ukrainian language.
### Approach
Mostly formal. More advanced ones are still quite faulty when implemented for Ukrainian and need much more resources.
### Reason
It almost physically hurts to read badly written articles. I decided to try to research the problem and create a potentially helpful solution.

## Technologies used
* python 3.9
* re
* pymorphy2
* json
* pathlib

## Structure of a project
* *text_uniformer* - a stand-alone program to clean all the leftovers of converting PDF files to TXT, it also formats the articles from different journals in the same way;
* *build_a_corpus*, *get_metadata*, *get_analysis* - a three-module program that extracts metadata of given articles, analyses their texts and creates corpora in JSON;
* *corpus - non processed* - TXT files of the corpus, converted from PDF (reviewed and edited manually);
* *corpus - processed* - TXT files of the corpus, after the use of text_uniformer;
* corpora in JSON:
  * *corpus_from_empty_file* - a testing file;
  * *corpus_of_science_articles* - all the articles are gathered in one file;
  * *statistics_of_science_articles* - all the numbers from the analyses are summed by type of journal or a journal;
  * *subcorpora_of_science_articles* - reorganised parts by type of journal and journals of the large corpus (Subcorpora folder has separate files corresponding with the parts because it is more efficient).

## Features
--- waiting to be written ---

## Project status
It is still in progress.

## Setup
--- waiting to be written ---

## Acknowledgements
--- waiting to be written ---

## Contact
Feel free to contact me at ivahnenko.bohdana@knu.ua
