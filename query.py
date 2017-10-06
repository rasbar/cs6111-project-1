#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 00:24:35 2017

@author: Parth
"""

import operator
import sys
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from googleapiclient.discovery import build

def createCSE(precision, query, api_key, engine_id):
    print("Parameters:\n" +
    "Client Key\t= " + api_key +
    "\nEngine Key\t= " + engine_id +
    "\nQuery\t\t= " + query +
    "\nPrecision\t= " + precision)
    service = build("customsearch", "v1",
                    developerKey=api_key)
    cse = service.cse().list(
            q=query, cx=engine_id)
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
            if(relevant in ["Y", "y"]):
                yesItems.append(item)
                break
            elif(relevant == "N" or relevant == "n"):
                noItems.append(item)
                break
            else:
                print("Invalid input")
    return yesItems, noItems

def start(precision, query, stopWords, api_key, engine_id):
    queryV = []
    for word in query.split(" "):
        queryV.append(word)
    cse = createCSE(precision, query, api_key, engine_id)
    res = cse.execute()
    yesItems, noItems = displayRes(res)
    evaluate(query, precision, yesItems, noItems, stopWords, queryV,
             api_key, engine_id)

def evaluate(query, precision, yesItems, noItems, stopWords, queryV,
             api_key, engine_id):
    print("======================")
    print("FEEDBACK SUMMARY")
    print("Query: ", query)
    print("Target precision: ", precision)
    precisionObtained = len(yesItems) / 10;
    print("Achieved precision: ", precisionObtained)
    if(precisionObtained >= float(precision)):
        print("Precision achieved. Stopping")
        return
    elif(precisionObtained == 0):
        print("No relevant documents. Stopping")
        return
    else:
        print("Perfoming next iteration")
        updateQuery(precision, query, yesItems, noItems, stopWords, queryV,
                    api_key, engine_id)

def createVectors(query, yesItems, noItems, stopWords):
    relevantV = dict()
    relevantTitleV = dict()
    notRelevantV = dict()
    rel = []
    relTitle = []
    tokenizer = RegexpTokenizer(r'\w+')
    wordnet_lemmatizer = WordNetLemmatizer()
    for item in yesItems:
        relTitle.append(item['title'])
        rel.append(item['snippet'])
    notRel = []
    for item in noItems:
        notRel.append(item['title'])
        notRel.append(item['snippet'])
    for item in rel:
        words = tokenizer.tokenize(item)
        for word in words:
            word = word.lower()
            word = wordnet_lemmatizer.lemmatize(word)
            if word not in stopWords:
                if word not in relevantV:
                    relevantV[word] = 0
                relevantV[word] += 1
    for item in relTitle:
        words = tokenizer.tokenize(item)
        for word in words:
            word = word.lower()
            word = wordnet_lemmatizer.lemmatize(word)
            if word not in stopWords:
                if word not in relevantTitleV:
                    relevantTitleV[word] = 0
                relevantTitleV[word] += 1
    for item in notRel:
        words = tokenizer.tokenize(item)
        for word in words:
            word = word.lower()
            word = wordnet_lemmatizer.lemmatize(word)
            if word not in stopWords:
                if word not in notRelevantV:
                    notRelevantV[word] = 0
                notRelevantV[word] += 1
    return relevantV, notRelevantV, relevantTitleV

def getTop2Words(sorted_list, queryV):
    top2 = []
    count = 0
    for key, value in sorted_list:
        if(count == 2):
            break
        if key not in queryV:
            top2.append(key)
            count += 1
    return top2

def rocchio(queryV, relevantV, notRelevantV, relCount, notRelCount, relevantTitleV):
    for key in relevantTitleV:
        relevantTitleV[key] *= (0.65 / relCount)
        
    for key in relevantV:
        relevantV[key] *= (0.75 / relCount)
    for key in notRelevantV:
        notRelevantV[key] *= (0.15 / notRelCount)

    for key in relevantTitleV: 
        if key in relevantV:
            relevantV[key] += relevantTitleV[key]
        else:
            relevantV[key] = relevantTitleV[key];

    for key in relevantV:
        if key in notRelevantV:
            relevantV[key] = max((relevantV[key] - notRelevantV[key]), 0)            
    
    sorted_list = sorted(list(relevantV.items()),
                         key=operator.itemgetter(1), reverse=True)
    return getTop2Words(sorted_list, queryV)

def updateQuery(precision, query, yesItems, noItems, stopWords, queryV,
                api_key, engine_id):
    relevantV = dict()
    relevantTitleV = dict()
    notRelevantV = dict()
    relCount = len(yesItems)
    notRelCount = len(noItems)
    relevantV, notRelevantV, relevantTitleV = createVectors(query, yesItems, noItems, stopWords)
    top2 = rocchio(queryV, relevantV, notRelevantV, relCount, notRelCount, relevantTitleV)
    print("Augmenting by  " + top2[0] + " " + top2[1])
    for word in top2:
        query = query + " " + word
    start(precision, query, stopWords, api_key, engine_id)

def getStopWords():
    stopWords = []
    fp = open('proj1-stop.txt', 'r')
    for line in fp:
        stopWords.append(line.rstrip())
    return stopWords

def main():
    api_key = sys.argv[1]
    engine_id = sys.argv[2]
    precision = sys.argv[3]
    query = sys.argv[4]
    stopWords = getStopWords()
    start(precision, query, stopWords, api_key, engine_id)

if __name__ == '__main__':
   main()
