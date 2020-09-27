import pathlib
import re

import setuptools

directory = pathlib.Path(__file__).parent.absolute()

# version
init_path = directory.joinpath("obonet", "__init__.py")
with init_path.open() as read_file:
    text = read_file.read()
pattern = re.compile(r"^__version__ = ['\"]([^'\"]*)['\"]", re.MULTILINE)
version = pattern.search(text).group(1)

# long_description
readme_path = directory.joinpath("README.md")
with readme_path.open() as read_file:
    long_description = read_file.read()

setuptools.setup(
    name="obonet",
    version=version,
    author="Daniel Himmelstein",
    author_email="daniel.himmelstein@gmail.com",
    url="https://github.com/dhimmel/obonet",
    project_urls={
        "Source": "https://github.com/dhimmel/obonet",
        "Tracker": "https://github.com/dhimmel/obonet/issues",
    },
    description="Parse OBO formatted ontologies into networkx",
    long_description_content_type="text/markdown",
    long_description=long_description,
    license="BSD-2-Clause-Patent",
    packages=["obonet"],
    keywords="obo ontology networkx parser network",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: BSD License",
        # not a valid classifier. see https://github.com/pypa/trove-classifiers/issues/17
        # "License :: OSI Approved :: BSD 2-Clause Plus Patent License (BSD-2-Clause-Patent)",
        "Programming Language :: Python :: 3",
    ],
    # Dependencies
    python_requires=">=3",
    install_requires=[
        "networkx",
    ],
)
