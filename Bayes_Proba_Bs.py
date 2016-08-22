# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 09:54:33 2016

@author: Manon Verdier
"""
import numpy as np

from scipy.misc import factorial
from itertools import product


def combi(seq,Nbr_parent):
    """
    Returns all the arrangements that can possibly have the set of parents
    *** Parameters :
    * seq : set of values that can take the parents.
    * Nbr_parent : Number of parents that has the variable
    """
    return [p for p in product(seq, repeat=Nbr_parent)]
    
    
def parent(Bs,i):
    """
    Returns the set of parents of the variable i
    *** Parameters :
    * Bs : np.array, adjency matrix
    * i : int, number of the variable 
    """
    c=Bs[:,i]
    
    pi=[]
    for l in range(len(c)):
        if c[l]==1 and l!=i:
            pi=np.append(pi,l)
    return pi


def N_ijk (D,Bs,i,j,k,ri):  
   pi=parent(Bs,i)
   
   c=D[:,i,:]
   count=0
   if len(pi)==0 :
      count=sum(c[:,k])
   else :

      comb=combi(np.arange(ri),len(pi))[j]
      count=c[:,k]
      
      for elm in range(len(pi)) :
          count=np.multiply(count,D[:,pi[elm],comb[elm]])

   return np.sum(count)

    
def N_ij (D,Bs,i,j, ri):
    Nij=0
    for k in range(0,ri):
        Nij+=N_ijk(D,Bs,i,j,k,ri)
    return Nij
    


def jk(D,Bs,i,j,frac,possible,ri):     

    Num=factorial(ri-1)
    Den=factorial(N_ij(D,Bs,i,j,ri)+ri-1)
    frac*=np.float128(Num)/np.float128(Den)

    for k in range(0,ri):
        frac*=factorial(N_ijk(D,Bs,i,j,k,ri))       
        if N_ijk(D,Bs,i,j,k,ri)!=0 :
            possible=1   

    return frac,possible   



def proba_Bs(Bs,D,ri,Nbr_data):       
    """
    Calculates the probability of the network Bs on the dataset D
    *** Parameters :
    * D : np.array, dataset
    * Bs : np.array, adjency matrix
    * ri : int, number of samples 
    * Nbr_data : Number of variables
    """
    P_Bs=1.0
    res=1.0
    possible=0
    
    for i in range (0,Nbr_data):
        frac=1.0
        pi=parent(Bs,i)
        qi=len(combi(np.arange(ri),len(pi)))
        
        if len(pi)==0 :
            j=1
            frac, possible=jk(D,Bs,i,j,frac,possible,ri)            
        else :
            for j in range(0,qi):
                frac, possible=jk(D,Bs,i,j,frac,possible,ri)
                
        res*=frac
      
    if possible==1:
        return P_Bs*res
    else : 
        return 0      
        
