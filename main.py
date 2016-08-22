from Bayesian_method import Bayesian_method


test=3

### Tests ### 

if test==1 :   

    Infile="Table_test_1.csv"
    Bsfile='Bs1.csv'
    
    Bayesian_method(Infile, Nbr_sampling=2, SamplingType='Value', method='Test',Bs_file=Bsfile)  
    
elif test==2:
    
    data_labels=['var1',
                 'var2',
                 'var3']
         
    Infile="Table_test_2.csv"
    
    Bayesian_method(Infile,data_labels,Nbr_max_parents=2, Nbr_sampling=3,method='Best_Random',Draw_graph=True)
    
elif test==3:
    data_labels=['var1',
                 'var2',
                 'var3']
         
    Infile="Table_test_2.csv"
    
    Bayesian_method(Infile,data_labels,Nbr_sampling=3, method='K2_emptymatrix',Draw_graph=True)