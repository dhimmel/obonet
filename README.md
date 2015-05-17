## A python parser for OBO ontology files

This repository contains python code for handling OBO serialized ontologies.

The function `obo.read_obo()` takes an `.obo` file and returns a [networkx MultiDiGraph](https://networkx.github.io/documentation/latest/reference/classes.multidigraph.html#networkx.MultiDiGraph) reprensentation of the ontology. The parser aims to be compatible with OBO versions [1.2](https://oboformat.googlecode.com/svn/trunk/doc/GO.format.obo-1_2.html) and [1.4](https://oboformat.googlecode.com/svn/trunk/doc/GO.format.obo-1_4.html).

We welcome feature suggestions and community contributions.
