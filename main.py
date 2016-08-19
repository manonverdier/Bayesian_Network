from Bayesian_method import Bayesian_method
import numpy as np


### Test 1 ### 

data_labels=['var1',
             'var2',
             'var3']


Infile="Table_test_1.csv"
Bsfile='Bs1.csv'

Bayesian_method(Infile, Nbr_sampling=2, SamplingType='Value', method='Test',Bs_file=Bsfile)  
