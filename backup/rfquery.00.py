#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

# System imports
import sys
import argparse
import pprint

# Google API imports
from googleapiclient.discovery import build

#------------------------------------------------------------------------------
# _main()
#------------------------------------------------------------------------------
def _main():

    # Parse cmdline to get program parameters
    apikey, cseid, precision, query = parse_cmdline()

    print('\nParameters:\nClient key = ', apikey, '\nEngine key = ', cseid,
            '\nQuery      = ', query, '\nPrecision  = ', precision)

    # Setup search engine with above parameters
    service = build("customsearch", "v1", developerKey=apikey)
    cse = service.cse().list(q=query, cx=cseid)

    # Run the query
    resdict = cse.execute()

    # Display results and get relevance feedback
    relevant, nonrelevant = get_relevance_feedback(resdict)

#------------------------------------------------------------------------------
# get_relevance_feedback(resdict)
#  Display query results and get relevance feedback on each item.
# Input:
#   resdict: dictionary output of search engine
# Output:
#   (relevant[], nonrelevant[]): lists of relevant and nonrelevant items
#------------------------------------------------------------------------------
def get_relevance_feedback(resdict):
    """Display query results and get relevance feedback."""

    items = resdict['items']
    relevant = []
    nonrelevant = []
    print("Google Search Results:\n"+"======================")
    for i in range(len(items)):
        item = items[i]
        print("Result " + str(i+1) + "\n[")
        print(" URL: " + item['formattedUrl'])
        print(" Title: " + item['title'])
        print(" Summary: " + item['snippet'])
        print("]")
        relevant = input("Relevant (Y/N)? ")
        if relevant == "Y":
            relevant.append(item)
        else:
            nonrelevant.append(item)

    return relevant, nonrelevant

#------------------------------------------------------------------------------
# parse_cmdline()
#   Simple command-line parser with help option to display usage info
#
# Input:
#   None
#
# Output:
#   tuple: (apikey, cseid, precision, query)
#------------------------------------------------------------------------------
def parse_cmdline():
    """Parse command-line."""

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
