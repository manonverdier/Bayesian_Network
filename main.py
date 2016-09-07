import ConfigParser
import os
from Bayesian_method import Bayesian_method

#Default values for the arguments
data_labels = 'None'
Nbr_max_parents = 3
Nbr_sampling = 3
SamplingType = 'Rank'
Weight_Sampling =  False
ListVarDiff='None'
Vectors='None'
method = 'K2_emptymatrix'
Bs_file = 'None'
NbrTests =  1000
NbrLinks_default = True
Draw_graph = False
Nbr_iter = 30
SaveFig=False
GeneratesFiles_toGraph=True
Nbr_Simulations=1000
NbrTests_annealing=10
withApriori=False
minSupport=0.15
minConfidence=0.9

#----------------------------

import sys

knownAnswer=False
ask_config=True

if len(sys.argv)>1:
    knownAnswer=True
    Answer=sys.argv[1]
    if Answer=='5' and len(sys.argv)>2:
        file_config=sys.argv[2]
        ask_config=False

parameters_labels=['data_labels','Nbr_max_parents','Nbr_sampling','SamplingType','Weight_Sampling','ListVarDiff','Vectors','method','Bs_file','NbrTests','NbrLinks_default','Draw_graph','Nbr_iter','SaveFig','GeneratesFiles_toGraph','Nbr_Simulations','NbrTests_annealing','withApriori','minSupport','minConfidence']
parameters=[data_labels,Nbr_max_parents,Nbr_sampling,SamplingType,Weight_Sampling, ListVarDiff,Vectors,method,Bs_file,NbrTests,NbrLinks_default,Draw_graph,Nbr_iter,SaveFig,GeneratesFiles_toGraph,Nbr_Simulations,NbrTests_annealing,withApriori,minSupport,minConfidence]


configParser = ConfigParser.RawConfigParser()


ans=True
while ans:
    if knownAnswer:
        ans=Answer
    else:
        print ("\n If you want to save your parameters for the option 5, please write a txt file following the examples of configuration_*.txt")
      
        print ("""
        1. Run test1 from configuration_1.txt
        2. Run test2 from configuration_2.txt
        3. Run test3 from configuration_3.txt     
        4. Run user's dataset and choose the parameters
        5. Run other configuration pre-defined (in configuration.txt)
        6. Exit/Quit
        """)
        ans=raw_input("Which option would you like to choose ? ")

    
    if ans=="6":
        print("\n Goodbye")
        ans=False
    elif int(ans)<1 and int(ans)>6:
        print("\n Not Valid Choice Try again") 
    else:
        if ask_config :
            if ans=='5':
                file_config=raw_input("What is the name of the configuration file (.txt) ?")
                    
            elif ans!='4' :
                file_config='configuration_'+ans+'.txt'
                          

        if ans!='4' :
            
            configFilePath = os.path.join(os.path.dirname(__file__), file_config)
            configParser.read(configFilePath)
            
            Infile = configParser.get('config', 'infile')
            print "\n Infile chosen : %s"  %Infile
            
            print "\n Changed parameters :"

            if configParser.has_option('config', 'data_labels'):
                parameters[0] = configParser.get('config', 'data_labels').split(",")
                print "data_labels chosen : " 
                print ' ' .join(parameters[0])   
           
           
            for param in range(1,len(parameters)) :	
                #It can be two types, treated appart.
                if parameters_labels[param] == "NbrLinks_default":
                    if configParser.has_option('config', 'NbrLinks_default'):
                        NbrLinks_default_arg = configParser.get('config', 'NbrLinks_default')                        
                        if NbrLinks_default_arg=='True': 
                            parameters[param] = True
                            print "Number max of variables that will have parents with Best_Random method : NbrLinks = Number of variables"
                        else: 
                            parameters[param] = configParser.getint('config', 'NbrLinks_default')
                            print "Number max of variables that will have parents with Best_Random method : NbrLinks = %d " %parameters[8]
                else:	
                    if configParser.has_option('config', parameters_labels[param]):
                        if isinstance(parameters[param],bool):
                            parameters[param]=configParser.getboolean('config', parameters_labels[param])
                            print parameters_labels[param]+" : %r" %parameters[param]
                        elif isinstance(parameters[param],int):
                            parameters[param]=configParser.getint('config', parameters_labels[param])
                            print parameters_labels[param]+" chosen : %d" %parameters[param]
                        elif isinstance(parameters[param],str):
                            parameters[param]=configParser.get('config', parameters_labels[param])
                            print parameters_labels[param]+" chosen : %s" %parameters[param]

         
        else : 
            print "Please type the name of the Infile (.csv) and type the parameters you want to change. Type enter if you want to keep the default ones. The Infile has to have the variables as columns and the cases as rows. \n"
            Infile=raw_input('Infile ? ')
            d=raw_input('Use default parameters ? y/n ')
            if d=='y' : 
                pass
            else : 
                for param in range(len(parameters)) : 
                    change=raw_input(str(parameters_labels[param])+' ?  (default = '+str(parameters[param])+') ')
                    if change=='':
                        pass
                    else : 
                        parameters[param]=change                       
        print '\n'
      
        data_labels = parameters[0]
        Nbr_max_parents = parameters[1]
        Nbr_sampling = parameters[2]
        SamplingType = parameters[3]
        Weight_Sampling =  parameters[4]
        ListVarDiff=parameters[5]
        Vectors=parameters[6]
        method = parameters[7]
        Bs_file = parameters[8]
        NbrTests = parameters[9] 
        NbrLinks_default = parameters[10]
        Draw_graph =parameters[11]
        Nbr_iter =parameters[12]
        SaveFig=parameters[13]
        GeneratesFiles_toGraph=parameters[14]
        Nbr_Simulations=parameters[15]
        NbrTests_annealing=parameters[16]
        withApriori=parameters[17]
        minSupport=parameters[18]
        minConfidence=parameters[19]
       
       
        Bayesian_method (Infile, data_labels, Nbr_max_parents, Nbr_sampling, SamplingType, Weight_Sampling, ListVarDiff,Vectors, method,Bs_file, NbrTests, NbrLinks_default,Draw_graph,Nbr_iter,SaveFig,GeneratesFiles_toGraph,Nbr_Simulations,NbrTests_annealing,withApriori,minSupport,minConfidence)
           
        ans=False

      
