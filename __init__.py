import requests
import pandas as pd
import re


class CountryEncoder:

    ''' This class is used to convert human-readable country names
        in arbitrary form (though spelling matters) into 3-letter ISO codes.
    '''

    def __init__(self, null_value=None):
        ''' Initialization: get the country name data,
            construct the vocabulary.
        '''
        self.stop_chars = re.compile(r'[^\w ]', re.UNICODE)
        self.stop_words = set(['of', 'the', 'and', 's'])
        self.null_value = null_value

        self.associative_matrix = pd.read_table('data.tsv', sep='\t', header=0)

    def rebuild_from_csv(self, file):
        ''' Rebuilds associative matrix JSON data
            from CSV source.
            Table format must be: name,full_name,alternative_name,abbreviation
        '''

    def tokenize(self, string):
        ''' Convert a string, human-readable country name,
            into a set of tokens.

            Returns: set
        '''
        string_lower = string.lower()
        bag = self.stop_chars.sub(' ', string_lower).split()
        return set(bag) - self.stop_words

    def encode(self, string):
        ''' Convert a human-readable country name
            to a 3-letter ISO country code.

            Returns: str
        '''
        country_bag = self.tokenize(string) & set(self.associative_matrix.columns)
        if len(country_bag) > 0:
            return self.associative_matrix[list(country_bag)].sum(axis=1).idxmax()
        else:
            return self.null_value
