# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 14:24:14 2016

@author: manon
"""
import pandas as pd
import numpy as np
import csv
from scipy.stats import cumfreq
import matplotlib.pyplot as plt

#!!!!!!!!!!! fichier est transposé : lignes=patients, colonnes=variables



def echantillonnage (fichier):

    data = np.genfromtxt(fichier,delimiter=',')
 
    clen, rlen = data.shape   
    new_tab=np.chararray([clen,rlen],itemsize=25)
 
    for c in range(0,rlen):
        petit=str(c)+'_1'
        moyen=str(c)+'_2'
        grand=str(c)+'_3'

        #----------------- sur le rang --------------------------
        data_sort=np.sort(data[:,c])
        x=len(data_sort)/3.
        tiers=data_sort[int(x)]
        deux_tiers=data_sort[2*int(x)]   
        #-----------------------------------------------------------        
        
        
        for l in range(0,clen):
            if data[l,c]<tiers:
                new_tab[l,c]=petit
                
            elif data[l,c]<deux_tiers:
                new_tab[l,c]=moyen
            else :
                new_tab[l,c]=grand
    
    return new_tab

def echantillonnage_glucose (fichier):

    data = np.genfromtxt(fichier,delimiter=',')  
    clen, rlen = data.shape   
    rlen=rlen+1
    diab= np.genfromtxt('glucose_a_traiter.csv',delimiter=',')
    new_tab=np.chararray([clen,rlen],itemsize=25)
 
    for c in range(0,rlen-1):
        petit=str(c)+'_1'
        moyen=str(c)+'_2'
        grand=str(c)+'_3'

        #----------------- sur le rang --------------------------
        data_sort=np.sort(data[:,c])
        x=len(data_sort)/3.
        tiers=data_sort[int(x)]
        deux_tiers=data_sort[2*int(x)]   
        #-----------------------------------------------------------        
        
        
        for l in range(0,clen):
            if data[l,c]<tiers:
                new_tab[l,c]=petit
                
            elif data[l,c]<deux_tiers:
                new_tab[l,c]=moyen
            else :
                new_tab[l,c]=grand
                
    for l in range (0,clen):        
        if diab[0,l]<6.5:            
            if diab[1,l]==0 and diab[2,l]==0 :
                new_tab[l,-1]=petit               
            else : 
                new_tab[l,-1]=moyen            
        else : new_tab[l,-1]=grand      
    
    return new_tab