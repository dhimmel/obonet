import os
import re
import subprocess

import setuptools


directory = os.path.dirname(os.path.abspath(__file__))

# version
init_path = os.path.join(directory, 'obonet', '__init__.py')
with open(init_path) as read_file:
    text = read_file.read()
pattern = re.compile(r"^__version__ = ['\"]([^'\"]*)['\"]", re.MULTILINE)
version = pattern.search(text).group(1)

# long_description
readme_path = os.path.join(directory, 'README.md')
try:
    # Try to create an reStructuredText long_description from README.md
    args = 'pandoc', '--from', 'markdown', '--to', 'rst', readme_path
    long_description = subprocess.check_output(args)
    long_description = long_description.decode()
except Exception as error:
    # Fallback to markdown (unformatted on PyPI) long_description
    print('README.md conversion to reStructuredText failed. Error:')
    print(error)
    with open(readme_path) as read_file:
        long_description = read_file.read()


setuptools.setup(
    name='obonet',
    version=version,
    author='Daniel Himmelstein',
    author_email='daniel.himmelstein@gmail.com',
    url='https://github.com/dhimmel/obonet',
    description='Parse OBO formatted ontologies into networkx',
    long_description=long_description,
    license='CC0 1.0',
    packages=['obonet'],

    keywords='obo ontology networkx parser network',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Programming Language :: Python :: 3',
    ],

    # Dependencies
    install_requires=[
        'networkx',
    ],
)
