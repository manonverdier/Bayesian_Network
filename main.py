import ConfigParser
import os
from Bayesian_method import Bayesian_method

#Default values for the arguments
data_labels = 'None'
Nbr_max_parents = 3
Nbr_sampling = 3
SamplingType = 'Rank'
Weight_Sampling =  False
method = 'K2_emptymatrix'
Bs_file = 'None'
NbrTests =  1000
NbrLinks_default = True
Draw_graph = False
Nbr_iter = 30
#----------------------------


parameters_labels=['data_labels','Nbr_max_parents','Nbr_sampling','SamplingType','Weight_Sampling','method','Bs_file','NbrTests','NbrLinks_default','Draw_graph','Nbr_iter']
parameters=[data_labels,Nbr_max_parents,Nbr_sampling,SamplingType,Weight_Sampling,method,Bs_file,NbrTests,NbrLinks_default,Draw_graph,Nbr_iter]
print parameters

configParser = ConfigParser.RawConfigParser()
configFilePath = os.path.join(os.path.dirname(__file__), 'configuration.txt')

configParser.read(configFilePath)

print ("\n Using configuration from configuration.txt file")

ans=True
while ans:
    print ("""
    0. Run user's dataset
    1. Run test1
    2. Run test2
    3. Run test3
    4. Exit/Quit
    """)
    ans=raw_input("Which test would you like to do? ")
    
    if ans=="4":
        print("\n Goodbye")
        ans=False
    elif int(ans)<0 and int(ans)>3:
        print("\n Not Valid Choice Try again") 
    else:
        if ans=='0':
            config_defined=raw_input("Did you define a configuration in the file configuration.txt ? y/n ")
            if config_defined=='y':
                name_config=raw_input("What is the name of the configuration ?")	

        else :
            name_config='test'+ans
            
        if ans!='0'or (ans=='0'and config_defined=='y') :

            Infile = configParser.get(name_config, 'infile')
            print "\n Infile chosen : %s"  %Infile

            if configParser.has_option(name_config, 'data_labels'):
                parameters[0] = configParser.get(name_config, 'data_labels').split(",")
                print "data_labels chosen : " 
                print ' ' .join(parameters[0])   
           
           
            for param in range(1,len(parameters)) :	
                #It can be two types, treated appart.
                if parameters_labels[param] == "NbrLinks_default":
                    if configParser.has_option(name_config, 'NbrLinks_default'):
                        NbrLinks_default_arg = configParser.get(name_config, 'NbrLinks_default')                        
                        if NbrLinks_default_arg=='True': 
                            parameters[param] = True
                            print "Number max of variables that will have parents with Best_Random method : NbrLinks = Number of variables"
                        else: 
                            parameters[param] = configParser.getint(name_config, 'NbrLinks_default')
                            print "Number max of variables that will have parents with Best_Random method : NbrLinks = %d " %parameters[8]
                else:	
                    if configParser.has_option(name_config, parameters_labels[param]):
                        if isinstance(parameters[param],bool):
                            parameters[param]=configParser.getboolean(name_config, parameters_labels[param])
                            print parameters_labels[param]+" : %r" %parameters[param]
                        elif isinstance(parameters[param],int):
                            parameters[param]=configParser.getint(name_config, parameters_labels[param])
                            print parameters_labels[param]+" chosen : %d" %parameters[param]
                        elif isinstance(parameters[param],str):
                            parameters[param]=configParser.get(name_config, parameters_labels[param])
                            print parameters_labels[param]+" chosen : %s" %parameters[param]

            print ('\n')
        else : 
            print "Please type the name of the Infile (.csv) and type the parameters you want to change. Type enter if you want to keep the default ones. The Infile has to have the variables as columns and the cases as rows. "
            Infile=raw_input('Infile ? ')
            d=raw_input('Use default parameters ? y/n ')
            if d=='y' : 
                pass
            else : 
                for param in range(len(parameters)) : 
                    change=raw_input(str(parameters_labels[param])+' ?  (Default = '+str(parameters[param])+') ')
                    if change=='':
                        pass
                    else : 
                        parameters[param]=change

      
        data_labels = parameters[0]
        Nbr_max_parents = parameters[1]
        Nbr_sampling = parameters[2]
        SamplingType = parameters[3]
        Weight_Sampling =  parameters[4]
        method = parameters[5]
        Bs_file = parameters[6]
        NbrTests =  parameters[7]
        NbrLinks_default = parameters[8]
        Draw_graph =parameters[9]
        Nbr_iter =parameters[10]
       
        Bayesian_method (Infile, data_labels, Nbr_max_parents, Nbr_sampling, SamplingType, Weight_Sampling, method,Bs_file, NbrTests, NbrLinks_default,Draw_graph,Nbr_iter)
           
        ans=False

      
