import setuptools

setuptools.setup(
    name = 'obo',
    version = '0.1.0',
    author = 'Daniel Himmelstein',
    author_email = 'daniel.himmelstein@gmail.com',
    url = 'https://github.com/dhimmel/obo',
    description = 'OBO ontology tools in python',
    license = 'CC0',
    packages = ['obo'],
    install_requires = ['networkx'],
    )
