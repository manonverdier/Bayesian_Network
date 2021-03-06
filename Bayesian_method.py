# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 14:09:16 2016

@author: Manon Verdier
"""
 
import numpy as np
import matplotlib.pyplot as plt
import itertools 

from sampling import sampling, sampling_wt
from Bayes_Find_Bs import K2, K2_emptymatrix, Bs_random, K2_add_to_matrix,Simulated_annealing

from Bayes_Proba_Bs import proba_Bs


def Bayesian_method(Infile,data_labels=None, Nbr_max_parents=3, Nbr_sampling=3, SamplingType='Rank', Weight_Sampling=False,   ListVarDiff='None', Vectors='None', method='K2_emptymatrix',Bs_file=None, NbrTests=1000, NbrLinks_default=True,Draw_graph=False,Nbr_iter=30,SaveFig=False,GeneratesFiles_toGraph=True,Nbr_Simulations=1000,NbrTests_annealing=10,withApriori=False,minSupport=0.15,minConfidence=0.9,Moy_RS=False):
    """
    Parameters:
    * Infile : csv file containing the dataset. Columns contain the variables 
               and the rows the cases. 
    
    ***** Optional
    * data_labels : list of the variables in the right order. Only used if Draw_graph=True
    * Nbr_max_parents : int, maximum number of parents for each variable. Default = 3
    * Nbr_sampling : int, number of classes to sample the data. Default = 3
    * SamplingType : {'Rank','Value'} 
        Method to sample the data
         - Rank : Default, sorts the data for each variable and samples it in Nbr_Sampling classes of same size.
         - Value : samples the data of each variable regarding the values of the data. The sample section will be (max-min)/Nbr_Sampling
    * Weight_Sampling : bool, to sample with weight. Default = False
    * ListVarDiff : csv file containing list of int, id numbers of the variables that need a different sampling, already known in Vectors. Only usable if Weight_Sampling=False. Default=None
    * Vectors : csv file containing list of vectors (of int), vectors contain the number of the group sampling of each case. The vectors oder has to respect the order of ListVarDiff.
                The first group is 0 and the last one is Nbr_sampling-1. Default = None
    * method : {'Random', 'Best_Random', 'K2', 'K2_emptymatrix','Test','Simulated_annealing'} 
        Method used to generate the network
         - Random : generates a random network.
         - Best_Random : keeps the best network out of NbrTests random networks.
         - K2 : greedy algorithm which keeps the network with the best score jk(). 
         - K2_emptymatrix : greedy algorithm which constructs the network with the 
           most probable parents, considering the other variables without parents. Default method.
         - K2_add_to_matrix : greedy algorithm which constructs the network by adding the 
           most probable parents to the parents already set up. 
         - Test : Mode to test a network Bs_test given as argument.
         - Simulated_annealing : simulated annealing algorithm that can be based on the results of Apriori algorithm if withApriori=True
    * Bs_file : csv file containing the adjacency matrix representing a network to test. Used only if the method='Test'.
    * NbrTests : int, number of networks tested with the Best_Random method. default = 1000
    * NbrLinks_default : True or int. Number max of variables that will have parents with the Random and the Best_Random method.
                         If True, the number is equal to the number of variables. Default = True.
    * Draw_graph : bool, to see the results as a directed graph with a Spring layout. Default = False. 
    * Nbr_iter : int, number of iterations for the Spring layout. Default = 30.
    * SaveFig : bool, will save the figure of the graph if Draw_graph is True. Default = False
    * GeneratesFiles_toGraph : bool, generates csv files to import the results in another graph visualization software (e.g Cystoscape). Default=True
    * Nbr_Simulations : int, number of iterations for the simulated annealing method. Default = 1000
    * NbrTests_annealing : int, number of simulated annealing graphs tested. All the Bs are saved in a csv file.
    * withApriori : bool, to use Apriori preteatment in the simulated annealing method. Default = False
    * minSupport : float, min support for the Apriori algorithm. Default = 0.15
    * minConfidence : float, min of confidance for the Apriori algorithm. Default = 0.9    
    * Moy_RS : bool, will generate the Bs for the average of NbrTests_annealing simulated annealing graphs which average are >0.5
    """

    ri=Nbr_sampling   

    print method

    
    if Weight_Sampling :
        D=sampling_wt(Infile,ri,SamplingType)    
    else :
        if ListVarDiff=='None' or Vectors=='None' :
            listVarDiff=[]
            vectors=[]
        else :             
            listVarDiff=np.genfromtxt(ListVarDiff,delimiter=',')
            if listVarDiff.size==1 :
                listVarDiff=[float(listVarDiff)]
                
            vectors=np.genfromtxt(Vectors,delimiter=',')
            
        D=sampling(Infile,ri,SamplingType,listVarDiff, vectors)#
        

    
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
            
    elif method=='Simulated_annealing' :
        import csv
        if withApriori :
            import AprioriPretreatment
            proba_matrix=AprioriPretreatment.AprioriPretreatment(Infile,minSupport,minConfidence,NbrTests_annealing,Nbr_Simulations)   
        else : proba_matrix=None
        for i in range(NbrTests_annealing) :
            Bs=Simulated_annealing(D,ri,Nbr_Simulations,Nbr_max_parents,withApriori,proba_matrix)              
            with open('Bs_SimA_'+Infile[:-4]+'_'+str(i)+'.csv', 'wb') as f:
                csv.writer(f).writerows(Bs)
            print  'Graph"s probability : ' + str(proba_Bs(Bs,D,ri,Nbr_data))
    else :
        raise NameError ('Incorrect method')
        
    if method!='Simulated_annealing' : 
        print  'Graph"s probability : ' + str(proba_Bs(Bs,D,ri,Nbr_data))
   
    
    tmps2=time.time()-tmps1
    
    print "Execution time = %f" %tmps2
   
    if Draw_graph and data_labels!='None' :
        
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
        
        if SaveFig : 
            plt.savefig('Graph_'+Infile[:-4]+'_'+method+'.pdf')
        plt.show()    
            #--------------------------------------------------------
   
    if Moy_RS :                
        #----------mean of 10 simulated annealing where we only keep the links > 0.5 

            Bs_i=np.empty((1,NbrTests_annealing),dtype=object)    
            for i in range(NbrTests_annealing):
                Bs_i[i]= np.genfromtxt('Bs_SimA_'+Infile[:-4]+'_'+str(i)+'.csv',delimiter=',')            

            Bs_moy=np.sum(Bs_i)/NbrTests_annealing
            Bs=np.zeros(Bs_moy.shape)
            Bs[Bs_moy>0.5]=Bs_moy[Bs_moy>0.5]      
   
   
    if GeneratesFiles_toGraph :
        import csv
        
        Nbr_data=len(data_labels)
        labels={}
        for i in range(len(data_labels)):
            labels[i]=data_labels[i]
          
        new_tab=np.zeros([Nbr_data,2],dtype=object)
        
        for i in range(0,Nbr_data):
            new_tab[i,0]=i+1
            new_tab[i,1]=data_labels[i]

        with open('to_cytoscape_labels_'+Infile[:-4]+'_'+method+'.csv', 'wb') as f:
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
        
        with open('to_cytoscape_Network_'+Infile[:-4]+'_'+method+'.csv', 'wb') as f:
            csv.writer(f).writerows(new)
                        
    
        
        
