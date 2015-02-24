"""
Indexes module. Contains the definitions of all classes used to index text
files (books).
"""
import re


class Index(object):
    """
    Interface class for different kinds of concrete Indexes that shares the
    same logic for the method distance().
    Field self.indexdict must be inizialized in derived concrete classes.
    """
    def distance(self, w1, w2):
        """
        Return the distance between two words if they are present in the
        calling index instance.
        Raise ValueError if invalid parameters are provided
        Raise ValueError if the strings provided are not in the index

        @param string w1  First word
        @param string w2  Second word

        """
        if not w1 or not w2:
            raise ValueError('Invalid word(s) given')
        if w1 == w2:
            raise ValueError('Words are the same')
        try:
            lst1 = self.indexdict[w1]
            lst2 = self.indexdict[w2]
        except KeyError as e:
            raise ValueError('Word {} is not in the index'.format(str(e)))

        # This loop finds the minimum distance of numbers present in the
        # ordered list lst1 and lst2 in linear time over the length of the list.
        i1 = 0
        i2 = 0
        mindist = self.indexdict[''][1]
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
        return len(self.indexdict) - 1

    def total_word_count(self):
        """
        Return the total number of words in the source text file.
        """
        if self.indexdict[''] != [0]:
            return self.indexdict[''][1] - 1
        else:
            return 0


class CaseSenIndex(Index):
    def __init__(self, filepath):
        self.indexdict = self._create_index(filepath)

    def _create_index(self, filepath):
        wordcounter = 0
        wordpos = {}
        # The file is readed and the position of each word is stored in a
        # dictionary such that key: word, value: list of all the positions of
        # that word in the source text file.
        with open(filepath, 'r') as f:
            for word in re.split('\W+', f.read()):
                if word in wordpos:
                    wordpos[word].append(wordcounter)
                else:
                    wordpos.update({word: [wordcounter]})
                wordcounter += 1                
        return wordpos


class CaseInsIndex(Index):
    def __init__(self, filepath):
        self.indexdict = self._create_index(filepath)

    def _create_index(self, filepath):
        # The file is readed and the position of each word is stored in a
        # dictionary such that key: word (forced lowercase), value: list of all
        # the positions of that word in the source text file (the case is
        # ignored).
        wordcounter = 0
        wordpos = {}
        with open(filepath, 'r') as f:
            for word in re.split('\W+', f.read()):
                word = word.lower()
                if word in wordpos:
                    wordpos[word].append(wordcounter)
                else:
                    wordpos.update({word: [wordcounter]})
                wordcounter += 1                
        return wordpos

    def distance(self, w1, w2):
        """
        Return the distance between two words if they are present in the
        calling index instance.
        Raise ValueError if invalid parameters are provided
        Raise ValueError if the strings provided are not in the index

        @param string w1  First word
        @param string w2  Second word

        The input is formatted to lowercase.
        """
        return super(CaseInsIndex, self).distance(w1.lower(), w2.lower())

