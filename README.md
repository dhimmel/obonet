[![Build Status](https://travis-ci.org/dhimmel/obo.svg?branch=master)](https://travis-ci.org/dhimmel/obo)

## A python parser for OBO ontology files

This repository contains python code for handling OBO serialized ontologies.

The function `obo.read_obo()` takes an `.obo` file and returns a [networkx MultiDiGraph](http://networkx.readthedocs.io/en/stable/reference/classes.multidigraph.html) representation of the ontology.
The parser aims to be compatible with OBO versions [1.2](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_2.html) and [1.4](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_4.html).

We welcome feature suggestions and community contributions.
