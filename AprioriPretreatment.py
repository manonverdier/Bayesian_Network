# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 15:40:46 2016

@author: manon
"""

import numpy as np
import csv 

from lien_apriori import dataFromFile,runApriori,printResults
from echantillonnage_apriori import echantillonnage


def AprioriPretreatment (Filedata,minSupport,minConfidence,NbrTests_annealing,
                         Nbr_Simulations):
    
    #-------------------Echantillonnage---------------------
    
    array=echantillonnage(Filedata)
    with open('to_apriori.csv', 'wb') as f:
        csv.writer(f).writerows(array)
        
    #-------------------Apriori-----------------------------
    
    inFile=dataFromFile('to_apriori.csv')
    items, rules = runApriori(inFile, minSupport, minConfidence)
    printResults(items, rules)
    
    #----------------- Matrice probabilité ------------------      
    
    def proba_matrix (rules,rlen):
        matrix=np.ones([rlen,rlen])
        for i in range(rlen):
            matrix[i,i]=0
        for j in range(len(rules)):
            a=rules[j,0]
            b=rules[j,1]
            matrix[a,b]=5
        return matrix
    
    #-----------------------------------------------------------
    data = np.genfromtxt(Filedata,delimiter=',')
    clen, rlen = data.shape  
    rules=np.genfromtxt('CoupleAssocRules.csv',delimiter=',')
    
    return proba_matrix(rules,rlen)
    
 