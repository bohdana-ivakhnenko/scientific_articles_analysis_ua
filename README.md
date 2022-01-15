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
The corpora created with *build_a_corpus* program include such features: 
#### Metadata of an article
* **name of the jounal** the article was published in;
* **type** of that journal;
* list of **authors**;
* name of the **institution** the author or authors represent(s);
* **title** of the article;
* its **doi** code;
* its **УДК** (UDC) code;
* **year** of publication;
* lists of **keywords** in Ukrainian, English, and Russian;
* **annotations** in Ukrainian, English, and Russian;
* lists of **abbreviations** used in the article in Ukrainian and English;
* lists of **sources** in Ukrainian and English;
* lists of **references** in Ukrainian and English.

#### Text level
* number of **words** (excluding annotation, lists of sources, references etc.), their average and median length in symbols (hyphen wasn't counted);
* number of **sentences**, their average and median length in words;
* number of **paragraphs**, their average and median length in sentences;
* number of **subordinate clauses** (підрядні речення), average and median number of them per sentence + all the starting words counted and sorted;
* number of **functors** (прийменники, сполучники і частки), average and median number of them per sentence + all of them counted and sorted;
* number of **substantiated nouns** ending with -ння or -ття, average and median number of them per sentence + all of them counted (in the subjective case) and sorted;
* number of **reflective verbs** (they end with -тися or -ться), average and median number of them per sentence + all of them counted (in the base form) and sorted;
* number of **verbs in impersonal form** ending with -но or -то, average and median number of them per sentence + all of them counted and sorted;
* number of **modal words** (they express how the author treats the information or feels about it, only incerted ones were counted), average and median number of them per sentence + all of them counted and sorted;
* number of **first person pronouns**, average and median number of them per sentence + all of them counted (in the subjective case) and sorted;
* number of **punctuation marks**, average and median number of them per sentence + all of them counted and sorted;
* number of **drawing, tables, diagrams, graphs and examples** in the text;
* number of **lists**;
* **citation** volume in words (text in "");
* number of **people mentioned** in the text (apart from citations like [Darwin, 12] etc.) and the full list;
* **text** of the article (excluding annotation, lists of sources, references etc.). 

#### Paragraph level 
* number of **words**, their average and median length in symbols (hyphen wasn't counted);
* number of **sentences**, their average and median length in words;
* number of **subordinate clauses** (підрядні речення), average and median number of them per sentence + all the starting words counted and sorted;
* number of **functors** (прийменники, сполучники і частки), average and median number of them per sentence + all of them counted and sorted;
* number of **substantiated nouns** ending with -ння or -ття, average and median number of them per sentence + all of them counted (in the subjective case) and sorted;
* number of **reflective verbs** (they end with -тися or -ться), average and median number of them per sentence + all of them counted (in the base form) and sorted;
* number of **verbs in impersonal form** ending with -но or -то, average and median number of them per sentence + all of them counted and sorted;
* number of **modal words** (they express how the author treats the information or feels about it, only incerted ones were counted), average and median number of them per sentence + all of them counted and sorted;
* number of **first person pronouns**, average and median number of them per sentence + all of them counted (in the subjective case) and sorted;
* number of **people mentioned** in the paragraph (apart from citations like [Darwin, 12] etc.) and the full list;
* **text** of the paragraph;
* **sentenses** of the paragraph **analyses** results.

#### Sentence level
* number of **words**, their average and median length in symbols (hyphen wasn't counted);
* number of **subordinate clauses** (підрядні речення), all the starting words counted and sorted;
* number of **functors** (прийменники, сполучники і частки), all of them counted and sorted;
* number of **substantiated nouns** ending with -ння or -ття, all of them counted (in the subjective case) and sorted;
* number of **reflective verbs** (they end with -тися or -ться), all of them counted (in the base form) and sorted;
* number of **verbs in impersonal form** ending with -но or -то, all of them counted and sorted;
* number of **modal words** (they express how the author treats the information or feels about it, only incerted ones were counted), all of them counted and sorted;
* number of **first person pronouns**, all of them counted (in the subjective case) and sorted;
* number of **people mentioned** in the sentense (apart from citations like [Darwin, 12] etc.) and the full list;
* **text** of the sentense.

## Project status
It is still in progress.

## Setup
--- waiting to be written ---

## Acknowledgements
--- waiting to be written ---

## Contact
Feel free to contact me at ivahnenko.bohdana@knu.ua
