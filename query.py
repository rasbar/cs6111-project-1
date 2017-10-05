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

def query(cse, precision, query):
    res = cse.execute()
    yesItems, noItems = displayRes(res)
    return yesItems, noItems

def createCSE(precision, query):
    print("Parameters:\n" + "Query\t\t= " + query + "\nPrecision\t= " + precision)
    service = build("customsearch", "v1",
            developerKey="")
    cse = service.cse().list(q=query, cx="")
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

def start():

def main():
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    precision = sys.argv[1]
    query = sys.argv[2]
    cse = createCSE(precision, query)
    
    yesItems, noItems = query(cse, precision, query)
    evaluate(yesItems, noItems)
    print("Target precision: ", precision)
    print("Achieved precision: ", len(yesItems))
    if(len(yesItems) >= precision):
        print("Precision achieved. Stopping")
        return
    elif(len(yesItems) == 0):
        print("No relevant documents. Stopping")
        return
    else:
        print("Perfoming next iteration")
        updateQuery(precision, query)
        

if __name__ == '__main__':
   main()
