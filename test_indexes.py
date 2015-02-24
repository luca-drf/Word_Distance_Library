"""
Unit test module for indexes.
"""
import unittest
import os
from indexes import CaseSenIndex, CaseInsIndex


class TestIndexesWrongPath(unittest.TestCase):
    def setUp(self):
        self.filepath = 'wrong_path.txt'

    def test_create_index(self):
        self.assertRaises(IOError, CaseSenIndex, self.filepath)
        self.assertRaises(IOError, CaseInsIndex, self.filepath)


class TestIndexesEmpty(unittest.TestCase):
    def setUp(self):
        self.filepath = 'empty.txt'
        self.text = ''
        with open(self.filepath, 'w') as f:
            f.write(self.text)

    def tearDown(self):
        os.remove(self.filepath)

    def test_create_index(self):
        # In this test an empty index is created
        s = CaseSenIndex(self.filepath)
        i = CaseInsIndex(self.filepath)
        self.assertEqual(i.total_word_count(), 0)
        self.assertEqual(s.total_word_count(), 0)
        self.assertEqual(i.single_word_count(), 0)
        self.assertEqual(s.single_word_count(), 0)


    def test_distance_failure(self):
        i = CaseSenIndex(self.filepath)
        self.assertRaises(ValueError, i.distance, 'A', 'B')


class TestIndexesSimple(unittest.TestCase):
    # This simple test is to show how the algorithm work and that is correct
    def setUp(self):
        self.filepath = 'unittest_test_book.txt'
        self.text = """
                    The Tragedy of Hamlet

                    ACT I.
 
                    Scene I. Elsinore. A platform before the Castle.
 
                    [Francisco at his post. Enter to him Bernardo.]
 
                    Ber.
                    Who's there?
 
                    Fran.
                    Nay, answer me: stand, and unfold yourself.
 
                    Ber.
                    Long live the king!
 
                    Fran.
                    Bernardo?
 
                    Ber.
                    He.
 
                    Fran.
                    You come most carefully upon your hour.
 
                    Ber.
                    'Tis now struck twelve. Get thee to bed, Francisco.
                    """
        with open(self.filepath, 'w') as f:
            f.write(self.text)

    def tearDown(self):
        os.remove(self.filepath)

    def test_case_sen_create_index(self):
        i = CaseSenIndex(self.filepath)
        # The numbers are the positions of the words in the text file starting
        # from 1 to 61
        self.assertEqual(i.indexdict['ACT'], [5])
        self.assertEqual(i.indexdict['Francisco'], [15, 61])
        self.assertEqual(i.total_word_count(), 61)

    def test_case_ins_create_index(self):
        # This test shows the difference between case sensitive and insensitive
        # behavior
        i = CaseInsIndex(self.filepath)
        self.assertEqual(i.indexdict['the'], [1, 13, 38])
        self.assertEqual(i.indexdict['act'], [5])
        self.assertEqual(i.indexdict['francisco'], [15, 61])
        self.assertEqual(i.total_word_count(), 61)

    def test_case_sen_distance(self):
        i = CaseSenIndex(self.filepath)
        d = i.distance('The', 'Ber')
        self.assertEqual(d, 21)

    def test_case_ins_distance(self):
        i = CaseInsIndex(self.filepath)
        d = i.distance('The', 'Ber')
        self.assertEqual(d, 2)

    def test_distance_failure(self):
        i = CaseSenIndex(self.filepath)
        self.assertRaises(ValueError, i.distance, 'Cookies', 'Ber')
        self.assertRaises(ValueError, i.distance, '', 'Ber')
        self.assertRaises(ValueError, i.distance, 'Ber', None)
        self.assertRaises(ValueError, i.distance, 'Ber', 'Ber')



class TestIndexesBible(unittest.TestCase):
    def setUp(self):
        self.filepath = 'pg30.txt'

    def test_case_ins_distance(self):
        # This test is simply to show that the library can handle large books
        # correctly
        i = CaseInsIndex(self.filepath)
        self.assertTrue(i.distance('the', 'farm'), 5)
        self.assertTrue(i.distance('genesis', 'god'), 3)


if __name__ == '__main__':
    unittest.main()
