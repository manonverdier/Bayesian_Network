# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 17:06:35 2016

@author: manon
"""

import sys

from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser


def subsets(arr):
    """ Returns non empty subsets of arr"""

    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
        """calculates the support for items in the itemSet and returns a subset
       of the itemSet each of whose elements satisfies the minimum support"""
        _itemSet = set()
        localSet = defaultdict(int)
        
#correspond au apriori-gen d'IBM en créant un Set d'item fréquent au lieu 
# d'enlever les items non fréquents du set de candidats
        
        for item in itemSet:
                for transaction in transactionList:
                        if item.issubset(transaction):
                                freqSet[item] += 1
                                localSet[item] += 1
                                
# calcul le support de chacun des items sélectrionnés à l'étape précédente et
# et on ne garde que ceux dont le support est assez grand
                                
        for item, count in localSet.items():
                support = float(count)/len(transactionList)

                if support >= minSupport:
                        _itemSet.add(item)

        return _itemSet


def joinSet(itemSet, length):
        """Join a set with itself and returns the n-element itemsets"""
        return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


def getItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))              # Generate 1-itemSets
    return itemSet, transactionList


def runApriori(data_iter, minSupport, minConfidence):
    """
    run the apriori algorithm. data_iter is a record iterator
    Return both:
     - items (tuple, support)
     - rules ((pretuple, posttuple), confidence)
    """
    itemSet, transactionList = getItemSetTransactionList(data_iter)

    freqSet = defaultdict(int)
    largeSet = dict()
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport

    #assocRules = dict()
    # Dictionary which stores Association Rules

    oneCSet = returnItemsWithMinSupport(itemSet,
                                        transactionList,
                                        minSupport,
                                        freqSet)

    currentLSet = oneCSet
    k = 2
    while(currentLSet != set([])):
        largeSet[k-1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet,
                                                transactionList,
                                                minSupport,
                                                freqSet)
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
            """local function which Returns the support of an item"""
            return float(freqSet[item])/len(transactionList)

    toRetItems = []
#    for key, value in largeSet.items():
#        toRetItems.extend([(tuple(item), getSupport(item))
#                           for item in value])
    for key, value in largeSet.items():
        for item in value : 
            if len(item)==2 :
                    toRetItems.extend([(tuple(item), getSupport(item))])
#si en enelevant tous les subsets (un à un) d'un set, le set restant (remain) 
#est d'un support assez grand alors on considère que le subset=> remain subset 
  
    toRetRules = []
    for key, value in largeSet.items()[1:]:
        for item in value:
            if len(item)==2 :
                _subsets = map(frozenset, [x for x in subsets(item)])
                for element in _subsets:
                    remain = item.difference(element)
                    if len(remain) > 0:
                        confidence = getSupport(item)/getSupport(element)
                        if confidence >= minConfidence:
                            toRetRules.append(((tuple(element), tuple(remain)),
                                               confidence))
    return toRetItems, toRetRules



def printResults(items, rules):

    
    import numpy as np
    import csv
    
    new_tab=np.empty([1,2],dtype=object)
    for rule, confidence in sorted(rules, key=lambda (rule, confidence): confidence):
        pre, post = rule
        #print "Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence)
       
        new_tab=np.append(new_tab,[[pre[0][:-2],post[0][:-2]]],axis=0)
    
    new_tab=np.delete(new_tab, 0, 0)   
    with open('CoupleAssocRules.csv', 'wb') as f:
        csv.writer(f).writerows(new_tab)
        


def dataFromFile(fname):
        """Function which reads from the file and yields a generator"""
        file_iter = open(fname, 'rU')
        for line in file_iter:
                line = line.strip().rstrip(',')                         # Remove trailing comma
                record = frozenset(line.split(','))
                yield record



