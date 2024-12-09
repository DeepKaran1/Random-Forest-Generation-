Random Trees and Forest Generation
This repository contains implementations and the theoretical background for generating random labeled trees, forests, and outerplanar graphs uniformly at random. The algorithms are based on recursive counting formulas and combinatorial techniques.

Contents
Research Paper: The theoretical foundation for the implemented algorithms, including:
Generating trees using Prüfer sequences.
Klingsberg’s algorithm for tree construction.
Recursive methods for random labeled tree and forest generation.
Python Scripts:
Klinsberg-Algorith_implementation.py: Implements Klingsberg’s algorithm for tree construction based on Prüfer sequences.
Random-Tree-Generation.py: Generates random labeled trees using recursive counting formulas.
Random-forest-generation.py: Extends the tree generation logic to create random labeled forests.
How to Use
Requirements
Python 3.x
Required Libraries:
networkx
matplotlib
Install the required libraries using:

bash
Copy code
pip install networkx matplotlib
Running the Scripts
Klinsberg Algorithm:

bash
Copy code
python Klinsberg-Algorith_implementation.py
This script demonstrates how to construct a labeled tree from a given Prüfer sequence and visualize the construction process.

Random Tree Generation:

bash
Copy code
python Random-Tree-Generation.py
This script generates and visualizes a random labeled tree for a given number of vertices.

Random Forest Generation:

bash
Copy code
python Random-forest-generation.py
This script generates and visualizes a random labeled forest with multiple components.

Theory Overview
The research paper provides detailed explanations of the algorithms and their mathematical foundations:
Prüfer Sequences: A bijection between labeled trees and sequences of length 
𝑛
−
2
n−2.
Recursive Formulas: Counting labeled trees and forests using combinatorial principles.
Klingsberg's Algorithm: A linear-time approach to tree construction.
Visualizations
The scripts include visualization features using networkx and matplotlib, allowing you to observe the constructed trees and forests.

Example Output
Generated Tree:
Generated Forest:
Authors
Asish Mukhopadhyay
Karandeep Dhillon
References
A. Nijenhuis and H. S. Wilf, Combinatorial Algorithms for Computers and Calculators.
Alexey S. Rodionov and Hyunseung Choo, On generating random network structures: Trees.
Herbert S. Wilf, The uniform selection of free trees.
