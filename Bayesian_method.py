# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 14:09:16 2016

@author: Manon Verdier
"""
 
import numpy as np
import matplotlib.pyplot as plt
import itertools 

from sampling import sampling, sampling_wt
from Bayes_Find_Bs import K2, K2_emptymatrix, Bs_random, K2_add_to_matrix
from Bayes_Proba_Bs import proba_Bs


def Bayesian_method (Infile, data_labels=None, Nbr_max_parents=3, Nbr_sampling=3, SamplingType='Rank', Weight_Sampling=False, method='K2_emptymatrix',Bs_file=None, NbrTests=1000, NbrLinks_default=True,Draw_graph=False,Nbr_iter=30):
    """
    Parameters:
    * Infile : csv file containing the dataset. Columns contain the variables and the rows the cases. 
    
    ***** Optional
    * data_labels :  list of the variables in the right order. Only used if Draw_graph=True
    * Nbr_max_parents : int, maximum number of parents for each variable. Default = 3
    * Nbr_sampling : int, number of classes to sample the data. Default = 3
    * SamplingType : {'Rank','Value'} 
        Method to sample the data
         - Rank : Default, sorts the data for each variable and samples it in Nbr_Sampling classes of same size.
         - Value : samples the data of each variable regarding the values of the data. The sample section will be (max-min)/Nbr_Sampling
    * Weight_Sampling : bool, to sample with weight. Default = False
    * method : {'Random', 'Best_Random', 'K2', 'K2_emptymatrix','Test'} 
        Method used to generate the network
         - Random : generates a random network.
         - Best_Random : keeps the best network out of NbrTests random networks.
         - K2 : greedy algorithm which keeps the network with the best score jk(). 
         - K2_emptymatrix : greedy algorithm which constructs the network with the 
           most probable parents, considering the other variables without parents. Default method.
         - K2_add_to_matrix : greedy algorithm which constructs the network by adding the 
           most probable parents to the parents already set up. 
         - Test : Mode to test a network Bs_test given as argument.
    * Bs_file : csv file containing the adjacency matrix representing a network to test. Used only if the method='Test'.
    * NbrTests : int, number of networks tested with the Best_Random method. default = 1000
    * NbrLinks_default : True or int. Number max of variables that will have parents with the Random and the Best_Random method.
                         If True, the number is equal to the number of variables. Default = True.
    * Draw_graph : bool, to see the results as a directed graph with a Spring layout. Default = False. 
    * Nbr_iter : int, number of iterations for the Spring layout. Default = 30.
    """

    ri=Nbr_sampling   

    print method

    
    if Weight_Sampling :
        D=sampling_wt(Infile,ri,SamplingType)
    else :
        D=sampling(Infile,ri,SamplingType)
        

    
    clen , rlen, k = D.shape
    Nbr_data=rlen
    
    if NbrLinks_default is True : 
        NbrLinks=rlen
    elif isinstance(NbrLinks_default,int) : 
        NbrLinks=NbrLinks_default
    else : 
        raise TypeError ('NbrLinks has to instancied as True or an integer.') 
    

    #---------------------------------------------------------
    
    
    import time 
    tmps1=time.time()
    
    if method=='Random':
        Bs=Bs_random(D,NbrLinks,Nbr_max_parents)               
    elif method=='Best_Random':
        proba_Bs_max=0
        Bs_max=np.zeros([rlen,rlen])
        for m in range(NbrTests):
            Bs = Bs_random(D,NbrLinks,Nbr_max_parents)
            proba_test=proba_Bs(Bs,D,ri,Nbr_data)
            if proba_test>proba_Bs_max:
                proba_Bs_max=proba_test
                Bs_max=Bs
        Bs=Bs_max    
    elif method=='K2':
        Bs=K2(D,ri,Nbr_max_parents)   
    elif method=='K2_emptymatrix':
        Bs=K2_emptymatrix(D,ri,Nbr_max_parents)
    elif method=='K2_add_to_matrix':
        Bs=K2_add_to_matrix(D,ri,Nbr_max_parents)
    elif method=='Test' : 
        if Bs_file!='None' :
            Bs=np.genfromtxt(Bs_file,dtype=int, delimiter=',') 
        else :
            raise TypeError( 'Bs_file is incorrect. Test mode needs a csv file containing the adjency matrix to test. ')
            
    else :
        raise NameError ('Incorrect method')
        
        
    print  'Graph"s probability : ' + str(proba_Bs(Bs,D,ri,Nbr_data))
    
    
    
    tmps2=time.time()-tmps1
    
    print "Execution time = %f" %tmps2
   
    if Draw_graph and data_labels!=None :
        
        import networkx as nx
        
        labels={}
        for i in range(len(data_labels)):
            labels[i]=data_labels[i]
            
        
        G=nx.DiGraph() 
        G=nx.from_numpy_matrix(Bs, create_using=G)            
        pos=nx.spring_layout(G,iterations=Nbr_iter)                    
        C=nx.weakly_connected_component_subgraphs(G)
        
        c=['b','r','g','y','c','m','darkgoldenrod','#bc82bd','#001C7F','#f0f0f0','#8dd3c7','#EAEAF2','#C44E52','#003FFF','#B8860B','#81b1d2','#8dd3c7','#FFB5B8','#E5E5E5']
        listcol=itertools.cycle(c)
        
        for g in C:
            nx.draw_networkx_nodes(g,pos,node_size=200,node_color=listcol.next(),labels=labels)
            nx.draw_networkx_edges(g,pos)
            nx.draw_networkx_labels(g,pos, labels=labels)
        plt.axis('off')
        

