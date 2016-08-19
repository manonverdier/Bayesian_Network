# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 09:46:55 2016

@author: Manon Verdier
"""

import numpy as np

def sampling (Infile,Nbr_classes,SamplingType):
    """
    Generate a np.array containing the dataset sampled into Nbr_classes classes. 
    ***Parameters :
    * Infile : csv file containing the dataset. Columns contain the variables and the rows the cases. 
    * Nbr_classes : int, number of classes to sample the dataset
    * SamplingType : {'Rank','Value'} 
        Method to sample the data
         - Rank : Default, sorts the data for each variable and samples it in Nbr_classes classes of same size.
         - Value : samples the data of each variable regarding the values of the data. The sample section will be (max-min)/Nbr_Classes
    """
    data = np.genfromtxt(Infile,delimiter=',')
    clen, rlen = data.shape   

    new_tab=np.zeros([clen,rlen,Nbr_classes],dtype=float)
 
    for c in range(0,rlen): 
   
        #---------------------------------------------------
        sorter=np.zeros((Nbr_classes,1))
        
        if SamplingType=='Rank' :   
            data_sort=np.sort(data[:,c])
            x=len(data_sort)/Nbr_classes
            for num_classe in range(Nbr_classes) :    
                sorter[num_classe]=data_sort[(num_classe+1)*int(x)-1]
                
        elif SamplingType=='Value':
            data_=data[:,c]
            x=(max(data_)-min(data_))/Nbr_classes
            for num_classe in range(Nbr_classes) :
                sorter[num_classe]=min(data_)+(num_classe+1)*int(x)
        #---------------------------------------------------       
        

        for l in range(0,clen):
            found=0
            idx=0
            while idx<len(sorter) and found==0  :
                d=data[l,c]
                if d<=sorter[idx]:
                    new_tab[l,c,idx]=1.0                  
                    found=1
                idx+=1   
            if found==0 :
                new_tab[l,c,-1]=1.0
     

    return new_tab



def sampling_wt (Infile,Nbr_classes):
    """
    Generate a np.array containing the dataset sampled into Nbr_classes classes with a weight system. 
    ***Parameters :
    * Infile : csv file containing the dataset. Columns contain the variables and the rows the cases. 
    * Nbr_classes : int, number of classes to sample the dataset
    """

    def _wt(sorter_idx, sorter_idx_1,x):
        return (0.5*(sorter_idx-x))/(sorter_idx-sorter_idx_1)+0.5
    def wt(sorter_idx, sorter_idx_1,x):
        return 1-_wt(sorter_idx, sorter_idx_1,x)
        
    data = np.genfromtxt(Infile,delimiter=',')

    
    clen, rlen = data.shape   
    new_tab=np.zeros([clen,rlen,Nbr_classes],dtype=float)
 
    for c in range(0,rlen): 

      #----------------- sur le rang --------------------------
        data_sort=np.sort(data[:,c])
        x=len(data_sort)/(Nbr_classes*4)
        sorter=np.zeros((Nbr_classes*4,1))
        for num_classe in range(Nbr_classes*4) :    
            sorter[num_classe]=data_sort[(num_classe+1)*int(x)-1]

      #--------------------------------------------------------            
    
        for l in range(0,clen):
            found=0
            idx=4
            num=0
            while idx<len(sorter)-1 and found==0  :
                d=data[l,c]
                if sorter[idx-4]<d<=sorter[idx]:
                    if d>sorter[idx-1]:
                        new_tab[l,c,num]=wt(sorter[idx],sorter[idx-1],d)[0]
                        new_tab[l,c,num+1]=_wt(sorter[idx],sorter[idx-1],d)[0]
                    elif d<sorter[idx-3]:
                        new_tab[l,c,num-1]=wt(sorter[idx-3],sorter[idx-4],d)[0]
                        new_tab[l,c,num]=_wt(sorter[idx-3],sorter[idx-4],d)[0]
                    else :
                        new_tab[l,c,num]=1.0
                   
                    found=1
                num+=1
                idx+=4   
            if found==0 :
                if d<sorter[3]:
                    new_tab[l,c,0]=1.0
                else :
                    new_tab[l,c,Nbr_classes-1]=1.0

    return new_tab
#    
#print sampling_wt('test_ech.csv',4)
#D[np.nonzero(D)]=1
#D=array
#with open('file_wt.csv', 'wb') as f:
#    csv.writer(f).writerows(array)