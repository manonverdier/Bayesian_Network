# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 10:44:52 2016

@author: Manon Verdier
"""

import random
import numpy as np
import copy

from Bayes_Proba_Bs import jk,proba_Bs

def Bs_random (D,NbrLinks,Nbr_parents):
    """
    generates a random adjency matrix for the data D, with NbrLinks variables having Nb_parents parents.
        A variable cannot be parent with itself.
    *** Parameters : 
    * D : np.array of the dataset
    * NbrLinks : int, maximal number of variables that will have parents
    * Nbr_parents : int, maximal number of parents that have the variables.
    
    """
    
    clen , rlen,k = D.shape   
    Bs=np.zeros([rlen,rlen])
    Nbr_links=random.randint(0,NbrLinks)
    rand=random.sample(range(rlen), Nbr_links)      
    for c in rand:  
        Nbrparents=random.randint(0,Nbr_parents)
        Bs[random.sample(range(c)+range(c+1,rlen), Nbrparents) ,c]=1
    return Bs
    


def K2 (D,ri,u):
    """
    Returns the adjency matrix of the network with the best score jk(). 
    *** Parameters : 
    * D : np.array of the dataset
    * ri : int, number of samples 
    * u : int, number maximal of parents that can have a variable
    """
    clen , rlen,k = D.shape  
    Bs_final=np.zeros([rlen,rlen])   
    Nbr_data=rlen
    
    def Find_max_jk(D,Bs,i,j,possible,ri,fmax,pi):
        var_max=[]
        possible_max=possible
        for var in list(set(range(rlen))-set(pi)):
            Bs_max=copy.copy(Bs)
            Bs_max[var,i]=1
            f,possible=jk(D,Bs_max,i,j,1.0,possible,ri)  
            if f>fmax and possible==1:
                fmax=f
                var_max=var
                possible_max=possible
        return var_max,fmax,possible_max
             

    for i in range(0,Nbr_data):
        Bs=np.zeros([rlen,rlen])   
        j=1
        P0, possible0=jk(D,Bs,i,j,1.0,0,ri)

        OKToProceed=True
        fmax=0
        pi=[]
        while OKToProceed and len(pi)<u:           
            z,fmax,possible1=Find_max_jk(D,Bs,i,j,0,ri,fmax,pi)  
            if fmax>P0 and possible1==1:
                pi=np.append(pi,z)
                Bs[z,i]=1
            else : OKToProceed=False
            
        if len(pi)!=0:        
            Bs_final[list(pi),i]=1
                        
    
    return Bs_final
 
   

def K2_emptymatrix (D,ri,u):
    """
    Returns the adjency matrix of the network with the most probable parents, 
    considering the other variables without parents.
    *** Parameters : 
    * D : np.array of the dataset
    * ri : int, number of samples 
    * u : int, number maximal of parents that can have a variable
    """
    clen , rlen,k = D.shape  
    Bs_final=np.zeros([rlen,rlen])   
    Nbr_data=rlen
    
      
    def Find_max(D,Bs,i,j,ri,fmax,pi):
        var_max=[]
        possible=0
        for var in list(set(range(rlen))-set(pi)):
            Bs_max=copy.copy(Bs)
            Bs_max[var,i]=1
            f=proba_Bs(Bs_max,D,ri,Nbr_data) 
            if f>fmax:
                possible=1
                fmax=f
                var_max=var
        return var_max,fmax,possible
     
    for i in range(0,Nbr_data):
        Bs=np.zeros([rlen,rlen])  
        j=1
        P0=proba_Bs(Bs,D,ri,Nbr_data)

        OKToProceed=True
        fmax=0
        pi=[]
        possible=1
        while OKToProceed and len(pi)<u and possible :          
            z,fmax,possible =Find_max(D,Bs,i,j,ri,fmax,pi)  
            if fmax>P0 and possible :
                pi=np.append(pi,int(z))
                Bs[z,i]=1
            else : OKToProceed=False
            
        if len(pi)!=0:        
            Bs_final[list(pi),i]=1           
                                   
    return Bs_final    
    
    
    
    
def K2_add_to_matrix (D,ri,u):
    """
    Returns the adjency matrix of the network by adding the most probable 
    parents to the parents already set up.
    *** Parameters : 
    * D : np.array of the dataset
    * ri : int, number of samples 
    * u : int, number maximal of parents that can have a variable
    """        
    clen , rlen,k = D.shape  
    Nbr_data=rlen
    def Find_max(D,Bs,i,ri,fmax,pi):
        found=0
        varmax=[]
        for var in list(set(range(rlen))-set(pi)):    
            Bs_max=copy.copy(Bs)
            Bs_max[var,i]=1
            f=proba_Bs(Bs_max,D,ri,Nbr_data)
            if f>fmax :
                fmax=f
                Bmax=Bs_max
                found=1
                varmax=var
        if found==0:
            Bmax=Bs
        return fmax,Bmax,found,varmax
        
            
    Bs=np.zeros([rlen,rlen]) 
    for i in range(0,Nbr_data):
        P0=proba_Bs(Bs,D,ri,Nbr_data)
        OKToProceed=True
        fmax=0
        pi=[]
        possible=1
        while OKToProceed and len(pi)<u and possible :          
            fmax,Bs_,possible,z =Find_max(D,Bs,i,ri,fmax,pi)  
            if fmax>P0 and possible :
                pi=np.append(pi,int(z))
                Bs=Bs_
            else : OKToProceed=False
                                      
    return Bs    
    


    

 
