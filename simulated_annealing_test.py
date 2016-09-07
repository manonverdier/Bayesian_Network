# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 21:29:43 2016

@author: manon
"""
import numpy as np
import csv 

from lien_apriori import dataFromFile,runApriori,printResults
from echantillonnage_apriori import echantillonnage,echantillonnage_glucose
from Bayesian_method import Bayesian_method


data_labels=['Homocysteinemie'] #--
data_labels.append('Glucose_sang') #--
data_labels.append('Glucose_LCS') #--
data_labels.append('Hemoglobine_A1C')   #--
data_labels.append('Hemoglobine') #--
data_labels.append('SEGA_total') #--
data_labels.append('PIC_basal')    #6
data_labels.append('PIC_plateau')
data_labels.append('AMP_basal')
data_labels.append('AMP_plateau')
data_labels.append('Pss')
data_labels.append('Rcsf_dynamique')
data_labels.append('Rcsf_statique')
data_labels.append('debit_prod_LCS')
data_labels.append('RAP_basal')  #14
data_labels.append('resistance')  #--
data_labels.append('erreur_normalisee') #--
data_labels.append('PVI')  #17
data_labels.append('elastance')  #18
data_labels.append('MeanCort_L')  
data_labels.append('MeanCort_R') 
data_labels.append('MeanCort_gen') 
data_labels.append('Indice_diabetique') 
#data_labels=['PIC_basal']
#data_labels.append('PIC_plateau')    
#data_labels.append('AMP_basal') 
#data_labels.append('AMP_plateau')
#data_labels.append('Rcsf')
#data_labels.append('Elastance')
#data_labels.append('PVI')
#data_labels.append('Pss')
#data_labels.append('Debit_prod_LCS') 
#data_labels.append('Glucose_sang')
#data_labels.append('Hemoglobine_A1C') 
#data_labels.append('Glucose_LCS') 



Moy_RS=True
#---------------parameters-----------------------
Filedata='data_22.csv'

data_labels=data_labels
Nbr_max_parents=3
Nbr_sampling=3
SamplingType='Rank'
Weight_Sampling =  False
method='Simulated_annealing'
Bs_file = 'None'
NbrTests =  1000
NbrLinks_default = True
Draw_graph=False
Nbr_iter=30
SaveFig=False
GeneratesFiles_toGraph=True
Nbr_Simulations=1000
useDiabet=True
NbrTests_annealing=10
withApriori=True
minSupport=0.15
minConfidence=0.9

#-------------------Echantillonnage---------------------
if useDiabet :
    array=echantillonnage_glucose(Filedata)
else :
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

#-----------------------------------------------------------
data = np.genfromtxt(Filedata,delimiter=',')
clen, rlen = data.shape  
rules=np.genfromtxt('CoupleAssocRules.csv',delimiter=',')
with open('Matrix_probabilite.csv', 'wb') as f:
    csv.writer(f).writerows(proba_matrix(rules,rlen))


Bayesian_method (Filedata, data_labels, Nbr_max_parents, Nbr_sampling, SamplingType, Weight_Sampling, method,Bs_file, NbrTests, NbrLinks_default,Draw_graph,Nbr_iter,SaveFig,GeneratesFiles_toGraph,Nbr_Simulations,useDiabet,NbrTests_annealing,withApriori,minSupport,minConfidence)
        

                 
if Moy_RS :                
#----------Moyenne des 10 recuits simulés dont on ne garde que les liens>0.5
#                 + génère les fichiers de ce réseau pour cytoscape
                     
    Bs0= np.genfromtxt('Bs_SimA_'+Filedata[:-4]+'_0.csv',delimiter=',')
    Bs1= np.genfromtxt('Bs_SimA_'+Filedata[:-4]+'_1.csv',delimiter=',')
    Bs2= np.genfromtxt('Bs_SimA_'+Filedata[:-4]+'_2.csv',delimiter=',')
    Bs3= np.genfromtxt('Bs_SimA_'+Filedata[:-4]+'_3.csv',delimiter=',')
    Bs4= np.genfromtxt('Bs_SimA_'+Filedata[:-4]+'_4.csv',delimiter=',')
    Bs5= np.genfromtxt('Bs_SimA_'+Filedata[:-4]+'_5.csv',delimiter=',')
    Bs6= np.genfromtxt('Bs_SimA_'+Filedata[:-4]+'_6.csv',delimiter=',')
    Bs7= np.genfromtxt('Bs_SimA_'+Filedata[:-4]+'_7.csv',delimiter=',')
    Bs8= np.genfromtxt('Bs_SimA_'+Filedata[:-4]+'_8.csv',delimiter=',')
    Bs9= np.genfromtxt('Bs_SimA_'+Filedata[:-4]+'_9.csv',delimiter=',')

    Bs_moy=(Bs0+Bs1+Bs2+Bs3+Bs4+Bs5+Bs6+Bs7+Bs8+Bs9)/10
    Bs=np.zeros(Bs_moy.shape)
    Bs[Bs_moy>0.5]=Bs_moy[Bs_moy>0.5]   
    
    
    Nbr_data=len(data_labels)
    labels={}
    for i in range(len(data_labels)):
        labels[i]=data_labels[i]
      
    new_tab=np.zeros([Nbr_data,2],dtype=object)
    
    for i in range(0,Nbr_data):
        new_tab[i,0]=i+1
        new_tab[i,1]=labels[i]
    
    with open('to_cytoscape_labels_RS_moy_23.csv', 'wb') as f:
        csv.writer(f).writerows(new_tab)
    #--------------
        
    new=np.empty([1,2],dtype=object)
    for j in range(rlen) : 
        nnz=np.nonzero(Bs[j,:])[0]
        if len(nnz)!=0:
            for a in range(0,len(nnz)):
                new=np.append(new,[[j+1,nnz[:][a]+1]],axis=0)
        else :    
                new=np.append(new,[[j+1,-1]],axis=0)
    
    new=np.delete(new, 0, 0)   
    np.place(new,new==-1,None)
    
    with open('to_cytoscape_Network_RS_moy_23.csv', 'wb') as f:
        csv.writer(f).writerows(new)   