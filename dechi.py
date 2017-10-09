#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""Query augmentation using relevance feedback.

CS6111: Group 33, Project 1
Authors : Rashad Barghouti (rb3074)
          Parth Panchmatia (psp2137)
"""

# System imports
import sys
import argparse
import numpy as np

# API imports
from googleapiclient.discovery import build
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# Simple data structure to hold and pass program vars
class RelevanceFeedback:
    pass
#——————————————————————————————————————————————————————————————————————————————
def _main():
    """Program entry point."""

    # Create rf data structure
    rf = RelevanceFeedback()

    # Parse cmdline to get rf.apikey, rf.cseid, rf.target_precision, & rf.query
    parse_cmdline(rf)

    # Set up Google's custom search engine with API key
    rf.service = build("customsearch", "v1", developerKey=rf.apikey)

    # Load stop-words from file
    with open('stopwords.txt', 'r') as f:
        stopwords = f.read().split()

    enable_google_search = True
    while enable_google_search:

        # Run the query and get relevance feedback
        process_query(rf, do_search=enable_google_search)

        # Disable Google search until explicitly enabled again
        enable_google_search = False

        # Start indexing; create vectorizer object
        print("Indexing results ....")
        vectorizer = CountVectorizer(stop_words=stopwords)

        # Use 'title' and 'snippet' strings as document data
        rdata = [' '.join([d['title'], d['snippet']]) for d in rf.rlvt]
        nrdata = [' '.join([rf.nonrlvt['title'], rf.nonrlvt['snippet']])]

        # Construct vocabulary from all data
        vectorizer.fit(rdata + nrdata)

        # Get docterm matrix for relevant data and a vector for nonrelevant doc
        index = vectorizer.transform(rdata)
        nrvec = vectorizer.transform(nrdata)

        # Get cumulative term frequencies and subtract nonrelevant vector
        tf = index.sum(axis=0) - nrvec

        # Zero out negative frequencies
        #tf[tf < 0] = 0

        # Create list of (term, frequency) tuples and sort in descending order
        # on frequency values
        tf = list(zip(vectorizer.get_feature_names(), tf.getA1()))
        tf.sort(key=lambda tup:tup[1], reverse=True)
        #print('tf: {}'.format(tf))

        # Extract augmentation terms from the top of the sorted tf list. Don't
        # consider zero- or negative frequency terms.
        #
        # (Leave original query as a string, as oppsoed to spliting it into a
        # list object first. That way, the 'in' keyword will work as a limited
        # stemming tool, e.g., 'jaguar' in 'jaguars' will be True and help
        # avoid augmenting with the latter.)
        #
        augterms = []
        for term, freq in tf:
            if term not in rf.query and freq > 0:
                augterms.append(term)
            if len(augterms) == 2:
                break

        if not augterms:
            print("No query expansion terms are found. Terminating")
            sys.exit(0)

        print('Augmenting by: {}'.format(' '.join(augterms)))
        rf.query = ' '.join([rf.query] + augterms)
        print('Expanded query: {}'.format(rf.query))

        # enable CSE and run another iteration
        enable_google_search = True

#——————————————————————————————————————————————————————————————————————————————
def process_query(rf, do_search=False):
    """Run query and get relevance feedback on each search result.

    The function will terminate program execution if any of the following is
    detected:
     (1) fewer than 10 results from the Google search;
     (2) a KeyboardInterrupt exception (Ctrl-C)
     (3) no relevant results were found.

    Arguments:
    ---------
    rf        -- RelevanceFeedback data structure
    do_search -- boolean argument to explicitly enable a search on Google's
                  CSE (default: False).
    Returns:
    -------
    rf.rlvt[]  -- list of relevant results from this search iteration
    rf.nonrlvt -- highest ranked nonrelevant result from this search iteration

    """

    print('\nParameters:\nClient key = ', rf.apikey,
        '\nEngine key = ', rf.cseid, '\nQuery      = ', rf.query,
        '\nPrecision  = ', rf.target_precision)

    # Do the Google search
    if do_search:
        rsltdict = rf.service.cse().list(q=rf.query, cx=rf.cseid).execute()

    # If fewer than 10 results were returned, terminate
    if len(rsltdict['items']) < 10:
        print('Search fewer than 10 results. Terminating', file=sys.stderr)
        sys.exit(1)

    print('\nGoogle Search Results:\n======================')

    rf.rlvt = []
    rf.nonrlvt = {}
    for i, item in enumerate(rsltdict['items'], start=1):
        print('Result {}\n['.format(i))
        print(' URL: {}'.format(item['formattedUrl']))
        print(' Title: {}'.format(item['title']))
        print(' Summary: {}\n]'.format(item['snippet']))

        # Catch a Ctrl-C in case we want to stop early
        try:
            while True:
                answer = input("Relevant (Y/N)? ").lower()
                if answer == 'y':
                    rf.rlvt.append(item)
                    break;
                elif answer == 'n':
                    if not rf.nonrlvt:
                        rf.nonrlvt = item
                    break;
                else:
                    print('Invalid answer. Try again or Ctrl-C to exit.')

        except KeyboardInterrupt:
            print('\n<Ctrl-C> detected. Terminating.')
            sys.exit(0)

    # If no relevant items in the results, terminate
    if not rf.rlvt:
        print('No relevant items in the search results. Terminating.')
        sys.exit(0)

    print('\n=================\nFEEDBACK SUMMARY')

    precision = len(rf.rlvt)/10.0
    if precision < rf.target_precision:
        print('Query: {}'.format(rf.query))
        print('Precision: {:.1f}'.format(precision))
        print('Still below the desired precision of {}'
                .format(rf.target_precision))
    else:
        print('Precision: {:.1f}'.format(precision))
        print('Desired precision reached. Done!')
        sys.exit(0)

#——————————————————————————————————————————————————————————————————————————————
def parse_cmdline(rf):
    """Parse command-line.

    Input:
    -----
    rf -- RelevanceFeedback data structures

    This function parses the command-line and initializes rf.apikey, rf.cseid,
    rf.precision, rf.query.

    """

    d = 'Reformulate search query based on explicit relevance feedback.'
    parser = argparse.ArgumentParser(description=d, fromfile_prefix_chars='@')

    # Positional (required) arguments
    parser.add_argument('apikey', nargs=1, metavar='<google api key>',
            help="Search engine's API key")
    parser.add_argument('cseid', nargs=1, metavar='<google engine id>',
            help="Search engine's ID")
    parser.add_argument('precision', nargs=1, metavar='<precision>',
            help='precision@10 value', type=float)
    parser.add_argument('query', nargs=1, metavar='<query>',
            help='query string in quotes')

    # Parse command-line and return
    args = parser.parse_args()

    # Do a sanity check on the value of the desired precision
    precision = args.precision[0]
    if not 0.0 < precision <= 1.0:
        print('Invalid precision@10 value. Must be: 0.0 < precision@10 <= 1.0')
        sys.exit(0)

    rf.apikey, rf.cseid, = args.apikey[0], args.cseid[0]
    rf.target_precision, rf.query = precision, args.query[0]
#——————————————————————————————————————————————————————————————————————————————
# If running as standalone program, start at _main()
#——————————————————————————————————————————————————————————————————————————————
if __name__ == '__main__':
    _main()
