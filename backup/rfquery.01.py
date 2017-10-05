#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""Query augmentation using relevance feedback.

CS6111: Project 1, Group 33
Author 1: Parth
Author 2: Rashad Barghouti (UNI:rb3074)
"""

# System imports
import sys
import argparse
from pathlib import Path
import pprint

# API imports
from googleapiclient.discovery import build
from sklearn.feature_extraction.text import CountVectorizer

#——————————————————————————————————————————————————————————————————————————————
def _main():
    """Program entry point."""

    # Parse cmdline to get program parameters
    apikey, cseid, precision, query = parse_cmdline()

    print('\nParameters:\nClient key = ', apikey, '\nEngine key = ', cseid,
            '\nQuery      = ', query, '\nPrecision  = ', precision)

    # Setup search engine with above parameters
    service = build("customsearch", "v1", developerKey=apikey)
    cse = service.cse().list(q=query, cx=cseid)

    # Run the query
    resdict = cse.execute()

    # For fast testing of 'per se' query
    relevant_items = [resdict['items'][0], resdict['items'][5],
                      resdict['items'][6], resdict['items'][8],
                      resdict['items'][9]]
    # Display search results and get relevance feedback lists
    #relevant_items, nonrelevant_items = get_rf_data(resdict)

    #print('\nRelevant: {}\tNonrelevant: {}\n'.format(len(relevant_items),
    #        len(nonrelevant_items)))
    # Construct document-text list
    # TODO: try adding title text along with snippet's
    docs = [item['snippet'] for item in relevant_items]

    #Add query to docs to vectorize
    docs.append(query)

    # Read minimal stopword list from local file
    from pathlib import Path
    p = Path('.') / 'minimal-stop-pylist.txt'
    stopwords = eval(p.read_text())

    # Create CountVectorizer object anc construct doc-term matrix/index
    vectorizer = CountVectorizer(stop_words=stopwords)
    dtindex = vectorizer.fit_transform(docs)
    print('Index dims: {}'.format(dtindex.shape))

    #pprint.pprint(relevant_items)

#——————————————————————————————————————————————————————————————————————————————
def get_rf_data(resdict):
    """Display query results and get relevance feedback on each.

    The function will terminate program execution if any of the following is
    detected:
     (1) fewer than 10 results from the Google search;
     (2) a KeyboardInterrupt exception (Ctrl-C)
     (3) no relevant results.

    Arguments:
    —————————
    resdict:
      Dictionary of results as returned by the Google search

    Returns:
    ———————
    relevant_items[], nonrelevant_items[]:
      Tuple of lists that contain relevant and nonrelevant results
    """

    reslen = len(resdict['items'])

    # If fewer than 10 results were returned, terminate
    if reslen < 10:
        print('Search returned {} results. Terminating'.format(reslen),
                file=sys.stderr)
        sys.exit(1)

    print('\nGoogle Search Results:\n======================')

    relevant_items = []
    nonrelevant_items = []
    for i, item in enumerate(resdict['items'], start=1):
        print('Result {}\n['.format(i))
        print(' URL: {}'.format(item['formattedUrl']))
        print(' Title: {}'.format(item['title']))
        print(' Summary: {}\n]'.format(item['snippet']))

        # Catch a Ctrl-C in case we want to stop early
        try:
            while True:
                answer = input("Relevant (Y/N)? ").lower()
                if answer == 'y':
                    relevant_items.append(item)
                    break;
                elif answer == 'n':
                    nonrelevant_items.append(item)
                    break;
                else:
                    print('Invalid answer. Try again or Ctrl-C to exit.')
        except KeyboardInterrupt:
            print('<Ctrl-C> detected. Terminating.')
            sys.exit(0)

    # If no relevant items in the results, terminate
    if not relevant_items:
        print('No relevant items in the search results. Terminating.')
        sys.exit(0)

    return relevant_items, nonrelevant_items

#——————————————————————————————————————————————————————————————————————————————
def parse_cmdline():
    """Parse command-line.

    Returns:
    ———————
    (apikey, cseid, precision, query) -- tuple of parsed cmdline args
    """

    d = 'Reformulate search query based on explicit relevance feedback.'
    parser = argparse.ArgumentParser(description=d, fromfile_prefix_chars='@')

    # Positional (required) arguments
    parser.add_argument('apikey', nargs=1, metavar='<google api key>',
            help="Search engine's API key")
    parser.add_argument('cseid', nargs=1, metavar='<google engine id>',
            help="Search engine's ID")
    parser.add_argument('precision', nargs=1, metavar='<precision>',
            help='precision@10 value')
    parser.add_argument('query', nargs=1, metavar='<query>',
            help='query string in quotes')

    # Parse command-line and return
    args = parser.parse_args()
    return args.apikey[0], args.cseid[0], args.precision[0], args.query[0]

#------------------------------------------------------------------------------
# If running as a script, call entry point _main()
#------------------------------------------------------------------------------
if __name__ == '__main__':

    DEBUG = False
    if DEBUG:
        import pdb
        pdb.set_trace()
    _main()
