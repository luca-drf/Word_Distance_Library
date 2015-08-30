"""
Indexes module. Contains the definitions of all classes used to index text
files (books).
"""
import re
import collections


class Index(object):
    """
    Interface class for different kinds of concrete Indexes that shares the
    same logic for the method distance().
    Field self.indexdict must be inizialized in derived concrete classes.
    """
    def _read(self, stream):
        word_n = 0
        indexdict = collections.defaultdict(list)        
        for word in re.split('\W+', stream.read()):
            if word != '':
                word_n += 1
                word = self._process_word(word)
                indexdict[word].append(word_n)
        return indexdict, word_n 
        
    def _process_word(self, word):
        """ Method to specify a word processor called before inserting a word
        in the index and before querying the index. This method is ment to be
        overrided in derived classes that needs a different word processing."""
        return word

    def distance(self, w1, w2):
        """
        Return the distance between two words if they are present in the
        calling index instance.
        Raise ValueError if invalid parameters are provided
        Raise ValueError if the strings provided are not in the index

        @param string w1  First word
        @param string w2  Second word

        """
        w1 = self._process_word(w1)
        w2 = self._process_word(w2)
        
        if not w1 or not w2:
            raise ValueError('Invalid word(s) given')
        if w1 == w2:
            raise ValueError('Words are the same')
        if w1 not in self.indexdict:
            raise ValueError('Word {} is not in the index'.format(w1))
        if w2 not in self.indexdict:
            raise ValueError('Word {} is not in the index'.format(w2))

        # This loop finds the minimum distance of numbers present in the
        # ordered list lst1 and lst2 in linear time over the length of the list.
        i1 = 0
        i2 = 0
        lst1 = self.indexdict[w1]
        lst2 = self.indexdict[w2]

        mindist = self.word_n
        while i1 < len(lst1) and i2 < len(lst2):
            dist = abs(lst1[i1] - lst2[i2]) - 1
      
            if dist < mindist:
                mindist = dist
            if lst1[i1] < lst2[i2]:
                i1 += 1
            else:
                i2 += 1
        return mindist

    def single_word_count(self):
        """
        Returns the number of different words.
        """
        return len(self.indexdict)

    def total_word_count(self):
        """
        Return the total number of words in the source text file.
        """
        return self.word_n

class CaseSenIndex(Index):
    def __init__(self, stream):
        self.indexdict, self.word_n = self._read(stream)


class CaseInsIndex(Index):
    def __init__(self, stream):
        self.indexdict, self.word_n = self._read(stream)

    def _process_word(self, word):
        return word.lower()

