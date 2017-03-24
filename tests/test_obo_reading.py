import os

import pytest

import obo
import obo.read


directory = os.path.dirname(os.path.abspath(__file__))


def test_read_taxrank_file():
    """
    Test reading the taxrank ontology OBO file.
    """
    path = os.path.join(directory, 'data', 'taxrank.obo')
    with open(path, 'rt') as read_file:
        taxrank = obo.read_obo(read_file)
    assert len(taxrank) == 61
    assert taxrank.node['TAXRANK:0000001']['name'] == 'phylum'
    assert 'NCBITaxon:kingdom' in taxrank.node['TAXRANK:0000017']['xref']


@pytest.mark.parametrize('extension', ['', '.gz', '.bz2', '.xz'])
def test_read_taxrank_path(extension):
    """
    Test reading the taxrank ontology OBO file from paths. Includes reading
    compressed paths.
    """
    path = os.path.join(directory, 'data', 'taxrank.obo' + extension)
    taxrank = obo.read_obo(path)
    assert len(taxrank) == 61


@pytest.mark.parametrize('extension', ['', '.gz', '.bz2', '.xz'])
def test_read_taxrank_url(extension):
    """
    Test reading the taxrank ontology OBO file from paths. Includes reading
    compressed paths.
    """
    url = 'https://github.com/dhimmel/obo/raw/master/tests/data/taxrank.obo'
    url += extension
    taxrank = obo.read_obo(url)
    assert len(taxrank) == 61


def test_parse_tag_line_newline_agnostic():
    for line in ['saved-by: vw', 'saved-by: vw\n']:
        tag, value, trailing_modifier, comment = obo.read.parse_tag_line(line)
        assert tag == 'saved-by'
        assert value == 'vw'
        assert trailing_modifier is None
        assert comment is None


def test_parse_tag_line_with_tag_and_value():
    line = 'synonym: "ovarian ring canal" NARROW []\n'
    tag, value, trailing_modifier, comment = obo.read.parse_tag_line(line)
    assert tag == 'synonym'
    assert value == '"ovarian ring canal" NARROW []'
    assert trailing_modifier is None
    assert comment is None


def test_parse_tag_line_with_tag_value_and_comment():
    line = "is_a: GO:0005102 ! receptor binding\n"
    tag, value, trailing_modifier, comment = obo.read.parse_tag_line(line)
    assert tag == 'is_a'
    assert value == 'GO:0005102'
    assert trailing_modifier is None
    assert comment == 'receptor binding'


def test_parse_tag_line_with_tag_value_and_trailing_modifier():
    line = 'xref: UMLS:C0226369 {source="ncithesaurus:Obturator_Artery"}\n'
    tag, value, trailing_modifier, comment = obo.read.parse_tag_line(line)
    assert tag == 'xref'
    assert value == 'UMLS:C0226369'
    assert trailing_modifier == 'source="ncithesaurus:Obturator_Artery"'
    assert comment is None


def test_parse_tag_line_with_tag_value_trailing_modifier_and_comment():
    line = 'xref: UMLS:C0022131 {source="ncithesaurus:Islet_of_Langerhans"} ! Islets of Langerhans\n'  # noqa: E501
    tag, value, trailing_modifier, comment = obo.read.parse_tag_line(line)
    assert tag == 'xref'
    assert value == 'UMLS:C0022131'
    assert trailing_modifier == 'source="ncithesaurus:Islet_of_Langerhans"'
    assert comment == 'Islets of Langerhans'


def test_parse_tag_line_backslashed_exclamation():
    line = 'synonym: not a real example \!\n'
    tag, value, trailing_modifier, comment = obo.read.parse_tag_line(line)
    assert tag == 'synonym'
    assert value == 'not a real example \!'
