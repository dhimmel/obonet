# obonet: load OBO-formatted ontologies into networkx

[![GitHub Actions CI Build Status](https://img.shields.io/github/workflow/status/dhimmel/obonet/Build?label=actions&style=for-the-badge&logo=github&logoColor=white)](https://github.com/dhimmel/obonet/actions)  
[![Software License](https://img.shields.io/pypi/l/obonet?style=for-the-badge&logo=FreeBSD&logoColor=white)](https://github.com/dhimmel/obonet/blob/main/LICENSE)  
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge&logo=Python&logoColor=white)](https://github.com/psf/black)  
[![PyPI](https://img.shields.io/pypi/v/obonet.svg?style=for-the-badge&logo=PyPI&logoColor=white)](https://pypi.org/project/obonet/)  


Read OBO-formatted ontologies in Python.
`obonet` is

+ user friendly
+ no nonsense
+ pythonic
+ modern
+ simple and tested
+ lightweight
+ [`networkx`](https://networkx.readthedocs.io/en/stable/overview.html) leveraging

This Python 3.4+ package loads OBO serialized ontologies into networks.
The function `obonet.read_obo()` takes an `.obo` file and returns a [`networkx.MultiDiGraph`](https://networkx.github.io/documentation/stable/reference/classes/multigraph.html) representation of the ontology.
The parser was designed for the OBO specification version [1.2](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_2.html) & [1.4](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_4.html).

## Usage

This package is designed and tested on python ≥ 3.4.
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

## Installation

[![PyPI](https://img.shields.io/pypi/v/obonet.svg)](https://pypi.org/project/hetio/)

The recommended approach is to install the latest release from [PyPI](https://pypi.org/project/hetio/) using:

```sh
pip install obonet
```

However, if you'd like to install the most recent version from GitHub, use:

```sh
pip install git+https://github.com/dhimmel/obonet.git#egg=obonet
```

## Contributing

[![GitHub issues](https://img.shields.io/github/issues/dhimmel/obonet.svg)](https://github.com/dhimmel/obonet/issues)

We welcome feature suggestions and community contributions.
Currently, only reading OBO files is supported.
Please open an issue if you're interested in writing OBO files in Python.

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
