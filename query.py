#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 00:24:35 2017

@author: Parth
"""

# test

import pprint
import sys
from googleapiclient.discovery import build

def query():
    cse = createCSE()
    res = cse.execute()
    yesItems, noItems = displayRes(res)
    return yesItems, noItems

def createCSE():
    precision = sys.argv[1]
    query = sys.argv[2]
    print("Parameters:\n" + "Query\t\t= " + query + "\nPrecision\t= " + precision)
    service = build("customsearch", "v1",
            developerKey="AIzaSyAlKLHe1eAmug6XeTlQ1DxzOsPI4zax7Ms")
    cse = service.cse().list(q=query, cx="006096712590953604068:qoxtr78cjow")
    return cse

def displayRes(res):
    items = res['items']
    yesItems = []
    noItems = []
    print("Google Search Results:\n"+"======================")
    for i in range(len(items)):
        item = items[i]
        print("Result " + str(i+1) + "\n[")
        print(" URL: " + item['formattedUrl'])
        print(" Title: " + item['title'])
        print(" Summary: " + item['snippet'])
        print("]")
        relevant = input("Relevant (Y/N)?")
        if relevant == "Y":
            yesItems.append(item)
        else:
            noItems.append(item)
    return yesItems, noItems

def main():
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    yesItems, noItems = query()

if __name__ == '__main__':
   main()
