# obonet: load OBO-formatted ontologies into networkx

[![GitHub Actions CI Build Status](https://img.shields.io/github/actions/workflow/status/dhimmel/obonet/build.yaml?branch=main&label=actions&style=for-the-badge&logo=github&logoColor=white)](https://github.com/dhimmel/obonet/actions)  
[![Software License](https://img.shields.io/pypi/l/obonet?style=for-the-badge&logo=FreeBSD&logoColor=white)](https://github.com/dhimmel/obonet/blob/main/LICENSE)  
[![PyPI](https://img.shields.io/pypi/v/obonet.svg?style=for-the-badge&logo=PyPI&logoColor=white)](https://pypi.org/project/obonet/)  


Read OBO-formatted ontologies in Python.
`obonet` is

+ user friendly
+ succinct
+ pythonic
+ modern
+ simple and tested
+ lightweight
+ [`networkx`](https://networkx.readthedocs.io/en/stable/overview.html) leveraging

This Python package loads OBO serialized ontologies into networks.
The function `obonet.read_obo()` takes an `.obo` file and returns a [`networkx.MultiDiGraph`](https://networkx.github.io/documentation/stable/reference/classes/multigraph.html) representation of the ontology.
The parser was designed for the OBO specification version [1.2](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_2.html) & [1.4](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_4.html).

## Usage

See [`pyproject.toml`](pyproject.toml) for the minimum Python version required and the dependencies.
OBO files can be read from a path, URL, or open file handle.
Compression is inferred from the path's extension.
See example usage below:

```python
import networkx
import obonet

# Read the taxrank ontology
url = 'https://github.com/dhimmel/obonet/raw/main/tests/data/taxrank.obo'
graph = obonet.read_obo(url)

# Or read the xz-compressed taxrank ontology
url = 'https://github.com/dhimmel/obonet/raw/main/tests/data/taxrank.obo.xz'
graph = obonet.read_obo(url)

# Number of nodes
len(graph)

# Number of edges
graph.number_of_edges()

# Check if the ontology is a DAG
networkx.is_directed_acyclic_graph(graph)

# Mapping from term ID to name
id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
id_to_name['TAXRANK:0000006']  # TAXRANK:0000006 is species

# Find all superterms of species. Note that networkx.descendants gets
# superterms, while networkx.ancestors returns subterms.
networkx.descendants(graph, 'TAXRANK:0000006')
```

For a more detailed tutorial, see the [**Gene Ontology example notebook**](https://github.com/dhimmel/obonet/blob/main/examples/go-obonet.ipynb).

## Comparison

This package specializes in reading OBO files into a `newtorkx.MultiDiGraph`.
A more general ontology-to-NetworkX reader is available in the Python [nxontology package](https://github.com/related-sciences/nxontology) via the `nxontology.imports.pronto_to_multidigraph` function.
This function takes a `pronto.Ontology` object,
which can be loaded from an OBO file, OBO Graphs JSON file, or Ontology Web Language 2 RDF/XML file (OWL).
Using `pronto_to_multidigraph` allows creating a MultiDiGraph similar to the created by `obonet`,
with some differences in the amount of metadata retained.

The primary focus of the `nxontology` package is to provide an `NXOntology` class for representing ontologies based around a `networkx.DiGraph`.
NXOntology provides optimized implementations for computing node similarity and other intrinsic ontology metrics.
There are two important differences between a DiGraph for NXOntology and the MultiDiGraph produced by obonet:

1. NXOntology is based on a DiGraph that does not allow multiple edges between the same two nodes.
   Multiple edges between the same two nodes must therefore be collapsed.
   By default, it only considers _is a_ / `rdfs:subClassOf` relationships,
   but using `pronto_to_multidigraph` to create the NXOntology allows for retaining additional relationship types, like _part of_ in the case of the Gene Ontology.

2. NXOntology reverses the direction of relationships so edges go from superterm to subterm.
   Traditionally in ontologies, the _is a_ relationships go from subterm to superterm,
   but this is confusing.
   NXOntology reverses edges so functions such as _ancestors_ refer to more general concepts and _descendants_ refer to more specific concepts.

The `nxontology.imports.multidigraph_to_digraph` function converts from a MultiDiGraph, like the one produced by obonet, to a DiGraph by filtering to the desired relationship types, reversing edges, and collapsing parallel edges.

## Installation

The recommended approach is to install the latest release from [PyPI](https://pypi.org/project/obonet/) using:

```sh
pip install obonet
```

However, if you'd like to install the most recent version from GitHub, use:

```sh
pip install git+https://github.com/dhimmel/obonet.git#egg=obonet
```

## Contributing

[![GitHub issues](https://img.shields.io/github/issues/dhimmel/obonet.svg?style=for-the-badge)](https://github.com/dhimmel/obonet/issues)

We welcome feature suggestions and community contributions.
Currently, only reading OBO files is supported.

## Develop

Some development commands:

```bash
# create virtual environment
python3 -m venv ./env

# activate virtual environment
source env/bin/activate

# editable installation for development
pip install --editable ".[dev]"

# install pre-commit hooks
pre-commit install

# run all pre-commit checks
pre-commit run --all

# run tests
pytest

# generate changelog for release notes
git fetch --tags origin main
OLD_TAG=$(git describe --tags --abbrev=0)
git log --oneline --decorate=no --reverse $OLD_TAG..HEAD
```

Maintainers can make a new release at <https://github.com/dhimmel/obonet/releases/new>.
