Word Distance Library
=====================
A simple coding exercise in Python.

Coding Task
-----------
Given a book, and two words from that book, create a method to give the
smallest number of words between those two words.  Assume that the book is
large (over 500 pages) and memory usage and performance is a concern.

Presentation
------------
Since the expected files are potentially very large I decided for an approach
that delivers good performances in repeated queries over the same file.

The book is first readed from the filesystem and then indexed producing a
dictionary (hash table) where the keys are the single words in the text and the
values are lists of integers. Each integer represent a position in the
text file occupied by the keyword.
The text file is parsed in one passage from begin to end and therefore the
lists in the hash table are incrementally built thus the numbers are ordered.

Then when the `distance()` method is called with two words, the algorithm will 
find the minimum distance between the two words in linear time over the length
of the lists (worst case: the longest list of the two returned by the hash
table).

So the overall complexity is should be linear on the dimension of the file (it
might suffer from heavy overhead depending how hash tables are updated
internally), however, the dictionary have to be created only once per 
file, then it can be stored or cached removing the indexing overhead.

In the `indexes.py` three classes are implemented, an interface (Index) and two
concrete classes (CaseSenIndex and CaseInsIndex) providing respectively a case
sensitive behavior and a case insensitive behavior. (Strategy Pattern)

The other three files are a set of unit tests (`test_indexes.py`), an command
line tool to use the distance function (`word_distance.py`) and a text file
containing The Bible for testing purpose (`pg30.txt`).

Requirements
------------
- Python (2.7 or 3.4)


Test
----
The file test_indexes.py contains all the unit tests for the indexes classes.
To run the tests, `cd` in the directory containing the project files:

    % python -m unittest discover

Command line tool usage
-----------------------
The file word_distance.py provides a command line interface for the distance()
method. To use the interface `cd` in the directory containing the project's
files and:

    % python word_distance.py [-h] -f FILE [-C] first_word second_word

The `-h` options will display the help:
    
        Word Distance Tool

    positional arguments:
      first_word            First word
      second_word           Second word

    optional arguments:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  Path of the text file containing the book
      -C                    Case sensitive search

Author
------
Copyright (C) 2015 Luca Da Rin Fioretto <radome@gmail.com>
