# BayesianNetwork

Python implementation of the algorithm presented in the paper *"A Bayesian Method for the Induction of Probalistic Networks from Data"* from Gregory F. Cooper and Edward Herskovits (1992).

This algorithm generates a high probability network for a dataset. The results can be visualized as graphs, and files can be generated in order to import the network in a visualization graph software such as Cytoscape. The algorithm can be run using the following methods, cf. the wiki page for more information :

* [Random](https://github.com/manonverdier/Bayesian_Network/wiki#random)
* [Best_Random](https://github.com/manonverdier/Bayesian_Network/wiki#best_random)
* [K2](https://github.com/manonverdier/Bayesian_Network/wiki#K2)
* [K2_emptymatrix](https://github.com/manonverdier/Bayesian_Network/wiki#K2_emptymatrix) 
* [K2_add_to_matrix](https://github.com/manonverdier/Bayesian_Network/wiki#K2_add_to_matrix)


## Usage

To run the code, you can type the following lines, and follow the instructions :

```
git clone https://github.com/manonverdier/Bayesian_Network.git
cd Bayesian_Network
python main.py	
```

The main file leads to a menu. 

1. Run test1
2. Run test2
3. Run test3 
4. Run user's dataset and choose the parameters
5. Run other configuration pre-defined (in configuration.txt)

There are 3 small tests available to verify the algorithm. 
For the option 4, you can run your dataset and enter the parameters directly when the instructions ask you to. The option 5 is after writting a new .txt configuration file in order to set your parameters and use them again. To know how to fill this file, pleaser refer to the [according section](https://github.com/manonverdier/Bayesian_Network/wiki#configurationtxt) in the wiki page.

If you already know how to use the code and want to skip the menu, you can add an option. The option corresponds to the number of the menu previously presented and goes from 1 to 5. If the option 5 is chosen, you can directly add the configuration name as a second option. Here are some examples. The following line will run the test 3.
```
python main.py 3
```
And this line will run the parameters configuration pre-defined in _configuration.txt_ named my_configuration. 
```
python main.py 5 my_configuration
```

The results of the tests should be :
* Test 1 : Probability = 2.23e-09
* Test 2 and 3 : Probability = 1.60e-12

The test 1 implements the example from Cooper's paper. The test 2 and 3 implement three variables. The first one is independant of the others, which are related : the third variable is equal to the second one plus 0.1. In the results, we are supposed to find again that : the graph show us the link between var2 and var3, and the independancy of var1.

## Dependencies 

- NumPy
- SciPy
- Random
- Copy 
- Itertools
- Os
- ConfigParser
- csv 
- sys

- Networkx (required if the print out is a graph, _i.e_ if Draw_graph=True)
- Matplotlib (required if the print out is a graph, _i.e_ if Draw_graph=True)

## Reference

- http://link.springer.com/article/10.1007/BF00994110


## Disclaimer

This software has been developed for research purposes only, and hence should not be used as a diagnostic tool. In no event shall the authors or distributors be liable to any direct, indirect, special, incidental, or consequential damages arising of the use of this software, its documentation, or any derivatives thereof, even if the authors have been advised of the possibility of such damage.



