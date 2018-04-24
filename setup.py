import pathlib
import re

import setuptools

directory = pathlib.Path(__file__).parent.absolute()

# version
init_path = directory.joinpath('obonet', '__init__.py')
with init_path.open() as read_file:
    text = read_file.read()
pattern = re.compile(r"^__version__ = ['\"]([^'\"]*)['\"]", re.MULTILINE)
version = pattern.search(text).group(1)

# long_description
readme_path = directory.joinpath('README.md')
with readme_path.open() as read_file:
    long_description = read_file.read()

setuptools.setup(
    name='obonet',
    version=version,
    author='Daniel Himmelstein',
    author_email='daniel.himmelstein@gmail.com',
    url='https://github.com/dhimmel/obonet',
    description='Parse OBO formatted ontologies into networkx',
    long_description_content_type='text/markdown',
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
