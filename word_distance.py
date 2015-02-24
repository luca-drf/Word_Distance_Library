"""
Command line interface for Index.distance() method.
"""
import argparse
from indexes import CaseSenIndex, CaseInsIndex


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Word Distance Tool')

    parser.add_argument('-f', '--file', action="store", required=True,
                        help='Path of the text file containing the book')
    parser.add_argument('-C', action="store_true",
                        help='Case sensitive search')
    parser.add_argument('first_word', action="store",
                        help='First word')
    parser.add_argument('second_word', action="store",
                        help='Second word')
    
    args = parser.parse_args()

    filepath = args.file
    try:
        if args.C:
            i = CaseSenIndex(filepath)
        else:
            i = CaseInsIndex(filepath)
        print (i.distance(args.first_word, args.second_word))
    except IOError as e:
        print (str(e))
    except ValueError as e:
        print(str(e))

    
