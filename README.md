# ChiMerge
Many classification algorithms require that the training data contain only discrete attributes. To use such an algorithm when there are numeric attributes, all numeric values must first be converted into discrete values---a process called discretization. This is an implementation of ChiMerge [1], a general, robust algorithm that uses the x2 statistic to discretize (quantize) numeric attributes.

## What's in this Repository
This repository contains the iris dataset that I've used to test the ChiMerge algorithm, and the python code of the algorithm.

## Installation and Usage
I have used Python 3.6.3 to develop and test the code, and have used only popular libraries such as numpy, pandas and math.

Once the libraries and environments are set up, the code can by run by executing 

```bash
python ChiMerge.py
```

## Description

## References
[1] Kerber, R., 1992, July. Chimerge: Discretization of numeric attributes. In *Proceedings of the tenth national conference on Artificial intelligence* (pp. 123-128). AAAI Press.
