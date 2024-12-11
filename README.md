# Random Trees and Forest Generation

This repository contains implementations and theoretical foundations for generating random labeled trees, forests, and outerplanar graphs uniformly at random. The algorithms are based on recursive counting formulas and combinatorial techniques.

## Contents

1. **[Research Paper](Research_paper.pdf)**  
   The theoretical foundation for the implemented algorithms, including:  
   - Generating trees using Prüfer sequences.  
   - Klingsberg’s algorithm for tree construction.  
   - Recursive methods for random labeled tree and forest generation.

2. **Python Scripts**:
   - `Klinsberg-Algorith_implementation.py`: Implements Klingsberg’s algorithm for tree construction based on Prüfer sequences.
   - `Random-Tree-Generation.py`: Generates random labeled trees using recursive counting formulas.
   - `Random-forest-generation.py`: Extends the tree generation logic to create random labeled forests.

## How to Use

### Requirements
- Python 3.x  
- Required Libraries:
  - `networkx`
  - `matplotlib`

Install the required libraries using:
```bash
pip install networkx matplotlib
```

Running the Scripts
To visualize Klingsberg's algorithm, run:
```bash

python Klinsberg-Algorithm_implementation.py
```

To generate a random labeled tree, run:
```bash

python Random-Tree-Generation.py
```
To generate a random labeled forest, run:
```bash

python Random-forest-generation.py
```

## References
This work builds upon foundational studies, including:

- **Nijenhuis and Wilf**: *Combinatorial Algorithms for Computers and Calculators*.
- **Wilf's paper**: *Uniform Selection of Free Trees*.
- Additional references are provided in the [research paper](Research_paper.pdf).
