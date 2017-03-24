import os
import re

import setuptools


directory = os.path.dirname(os.path.abspath(__file__))

# version
init_path = os.path.join(directory, 'obo', '__init__.py')
with open(init_path) as read_file:
    text = read_file.read()
pattern = re.compile(r"^__version__ = ['\"]([^'\"]*)['\"]", re.MULTILINE)
version = pattern.search(text).group(1)

setuptools.setup(
    name = 'obo',
    version = version,
    author = 'Daniel Himmelstein',
    author_email = 'daniel.himmelstein@gmail.com',
    url = 'https://github.com/dhimmel/obo',
    description = 'OBO ontology tools in python',
    license = 'CC0',
    packages = ['obo'],
    install_requires = ['networkx'],
    )
