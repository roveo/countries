import sys
import re
import pandas as pd


def tokenize(string):
    ''' Convert a string, human-readable country name,
        into a set of tokens.

        Returns: set
    '''
    stop_chars = re.compile(r'[^\w ]', re.UNICODE)
    stop_words = set(['of', 'the', 'and', 's', 'd', 'co'])
    string_lower = string.lower()
    bag = stop_chars.sub(' ', string_lower).split()
    return set(bag) - stop_words


def rebuild(filename):
    vocabulary = pd.read_table(filename, header=0, sep='\t').set_index('code')

    # bag as in 'bag of words'
    bags = vocabulary['name'].fillna('')
    bags += ' ' + vocabulary['full_name'].fillna('')
    bags += ' ' + vocabulary['abbreviation'].fillna('')
    bags += ' ' + vocabulary['alternative_name'].fillna('')
    bags = bags.apply(tokenize).to_dict()  # full set of all possible tokens for each country

    associative_matrix = pd.DataFrame()

    # combine all of the codes into a single matrix
    for code in bags:
        associative_matrix = pd.concat([associative_matrix, pd.DataFrame(index=(code, ), columns=bags[code]).fillna(1)])

    # normalize by distinctiveness: more distinctive token => closer to 1.
    for column in associative_matrix:
        associative_matrix[column] = associative_matrix[column] / associative_matrix[column].sum()

    # bonus for short names
    names = vocabulary['name'].fillna('').apply(tokenize).to_dict()
    for code in names:
        associative_matrix.ix[code, list(names[code])] += 1 / len(names[code])

    associative_matrix.index.name = 'code'

    return associative_matrix


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        rebuild(filename).reset_index().to_csv('data.tsv', sep='\t', index=False)
