#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 00:24:35 2017

@author: Parth
"""

import operator
import sys
from nltk.tokenize import RegexpTokenizer
from googleapiclient.discovery import build

def createCSE(precision, query):
    print("Parameters:\n" + "Query\t\t= " + query + "\nPrecision\t= " + precision)
    service = build("customsearch", "v1", 
                    developerKey="AIzaSyCqDEnJkCFVYJ2aF94ntsuEwUu1ofZRTLs")
    cse = service.cse().list(
            q=query, cx="009287071471840412963:zpb5-fjffom")
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
        while(True):
            relevant = input("Relevant (Y/N)?")
            if(relevant == "Y" or relevant == "y"):
                yesItems.append(item)
                break
            elif(relevant == "N" or relevant == "n"):
                noItems.append(item)
                break
            else:
                print("Invalid input")
    return yesItems, noItems

def start(precision, query, stopWords):
    queryV = []
    queryV.append(query)
    cse = createCSE(precision, query)
    res = cse.execute()
    yesItems, noItems = displayRes(res)
    evaluate(query, precision, yesItems, noItems, stopWords, queryV)

def evaluate(query, precision, yesItems, noItems, stopWords, queryV):
    print("Target precision: ", precision)
    print("Achieved precision: ", len(yesItems))
    if(len(yesItems) >= int(precision)):
        print("Precision achieved. Stopping")
        return
    elif(len(yesItems) == 0):
        print("No relevant documents. Stopping")
        return
    else:
        print("Perfoming next iteration")
        updateQuery(precision, query, yesItems, noItems, stopWords, queryV)

def createVectors(query, yesItems, noItems, stopWords):
    relevantV = dict()
    notRelevantV = dict()
    relCount = 0
    notRelCount = 0
    rel = []
    tokenizer = RegexpTokenizer(r'\w+')
    for item in yesItems:
        rel.append(item['title'])
        rel.append(item['snippet'])
    notRel = []
    for item in noItems:
        notRel.append(item['title'])
        notRel.append(item['snippet'])
    for item in rel:
        # words = item.split(" ")
        words = tokenizer.tokenize(item)
        # words = nltk.word_tokenize(item)
        for word in words:
            word = word.lower()
            if word not in stopWords:
                if word not in relevantV:
                    relevantV[word] = 0
                relevantV[word] += 1
                relCount += 1
    # print("relevantV")
    # print(relevantV)
    for item in notRel:
        words = tokenizer.tokenize(item)
        for word in words:
            word = word.lower()
            if word not in stopWords:
                if word not in notRelevantV:
                    notRelevantV[word] = 0
                notRelevantV[word] += 1
                notRelCount += 1
    return relevantV, notRelevantV
    
def getTop2Words(sorted_list, queryV):
    top2 = []
    count = 0
    # print(queryV)
    for key, value in sorted_list:
        if(count == 2):
            break
        # print(key)
        if key not in queryV:
            top2.append(key)
            count += 1
    return top2

def rocchio(queryV, relevantV, notRelevantV, relCount, notRelCount):
    print("queryV2")
    print(queryV)
    for key in relevantV:
        relevantV[key] *= (0.75 / relCount)
    for key in notRelevantV:
        notRelevantV[key] *= (0.15 / notRelCount)
    for key in relevantV:
        if key in notRelevantV:
            relevantV[key] = max((relevantV[key] - notRelevantV[key]), 0)
    sorted_list = sorted(list(relevantV.items()), 
                         key=operator.itemgetter(1), reverse=True)
    print("\n")
    print(sorted_list)
    print("\n")
    return getTop2Words(sorted_list, queryV)

def updateQuery(precision, query, yesItems, noItems, stopWords, queryV):
    relevantV = dict()
    notRelevantV = dict()
    relCount = len(yesItems)
    notRelCount = len(noItems)
    relevantV, notRelevantV = createVectors(query, yesItems, noItems, stopWords)
    top2 = rocchio(queryV, relevantV, notRelevantV, relCount, notRelCount)
    for word in top2:
        query = query + " " + word
    # print(query)
    start(precision, query, stopWords)

def getStopWords():
    stopWords = []
    fp = open('proj1-stop.txt', 'r')
    for line in fp:
        stopWords.append(line.rstrip())
    return stopWords

def main():
    # need to fix query with multiple words, because they would contain spaces
    precision = sys.argv[1]
    query = sys.argv[2]
    stopWords = getStopWords()
    start(precision, query, stopWords)

if __name__ == '__main__':
   main()
