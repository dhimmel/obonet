import os
import pathlib

import pytest

import obonet
from obonet.read import parse_tag_line

directory = os.path.dirname(os.path.abspath(__file__))


def test_read_taxrank_file() -> None:
    """
    Test reading the taxrank ontology OBO file.
    """
    pytest.importorskip("networkx", minversion="2.0")
    path = os.path.join(directory, "data", "taxrank.obo")
    with open(path) as read_file:
        taxrank = obonet.read_obo(read_file)
    assert len(taxrank) == 61
    assert taxrank.nodes["TAXRANK:0000001"]["name"] == "phylum"
    assert "NCBITaxon:kingdom" in taxrank.nodes["TAXRANK:0000017"]["xref"]


@pytest.mark.parametrize("extension", ["", ".gz", ".bz2", ".xz"])
@pytest.mark.parametrize("pathlike", [False, True])
def test_read_taxrank_path(extension: str, pathlike: bool) -> None:
    """
    Test reading the taxrank ontology OBO file from paths. Includes reading
    compressed paths.
    """
    path = os.path.join(directory, "data", "taxrank.obo" + extension)
    if pathlike:
        path = pathlib.Path(path)  # type: ignore [assignment]
    taxrank = obonet.read_obo(path)
    assert len(taxrank) == 61


@pytest.mark.parametrize("extension", ["", ".gz", ".bz2", ".xz"])
def test_read_taxrank_url(extension: str) -> None:
    """
    Test reading the taxrank ontology OBO file from paths. Includes reading
    compressed paths.
    """
    url = "https://github.com/dhimmel/obonet/raw/main/tests/data/taxrank.obo"
    url += extension
    taxrank = obonet.read_obo(url)
    assert len(taxrank) == 61


def test_read_brenda_subset() -> None:
    """
    Test reading a subset of the BrendaTissue.obo file. This file does not set
    the ontology tag. See <https://github.com/dhimmel/obonet/issues/10>.
    It also contains some unicode characters that should fail if not read as utf-8,
    see <https://github.com/dhimmel/obonet/issues/27>.
    """
    path = os.path.join(directory, "data", "brenda-subset.obo")
    brenda = obonet.read_obo(path)
    assert len(brenda) == 1
    assert "name" not in brenda.graph
    assert "ontology" not in brenda.graph
    assert "™⏸⟟⎞▹◬⽷⹽⫥⠷⩶⥣ⱸ♖⬭⌉⌐⦦" in brenda.graph["comment"][0]


@pytest.mark.parametrize("ontology", ["doid", "go", "pato"])
def test_read_obo(ontology: str) -> None:
    """
    Test that reading ontology does not error.
    """
    url = f"http://purl.obolibrary.org/obo/{ontology}.obo"
    graph = obonet.read_obo(url)
    assert graph


def test_parse_tag_line_newline_agnostic() -> None:
    for line in ["saved-by: vw", "saved-by: vw\n"]:
        tag, value, trailing_modifier, comment = parse_tag_line(line)
        assert tag == "saved-by"
        assert value == "vw"
        assert trailing_modifier is None
        assert comment is None


def test_parse_tag_line_with_tag_and_value() -> None:
    line = 'synonym: "ovarian ring canal" NARROW []\n'
    tag, value, trailing_modifier, comment = parse_tag_line(line)
    assert tag == "synonym"
    assert value == '"ovarian ring canal" NARROW []'
    assert trailing_modifier is None
    assert comment is None


def test_parse_tag_line_with_tag_value_and_comment() -> None:
    line = "is_a: GO:0005102 ! receptor binding\n"
    tag, value, trailing_modifier, comment = parse_tag_line(line)
    assert tag == "is_a"
    assert value == "GO:0005102"
    assert trailing_modifier is None
    assert comment == "receptor binding"


def test_parse_tag_line_with_tag_value_and_trailing_modifier() -> None:
    line = 'xref: UMLS:C0226369 {source="ncithesaurus:Obturator_Artery"}\n'
    tag, value, trailing_modifier, comment = parse_tag_line(line)
    assert tag == "xref"
    assert value == "UMLS:C0226369"
    assert trailing_modifier == 'source="ncithesaurus:Obturator_Artery"'
    assert comment is None


def test_parse_tag_line_with_tag_value_trailing_modifier_and_comment() -> None:
    line = 'xref: UMLS:C0022131 {source="ncithesaurus:Islet_of_Langerhans"} ! Islets of Langerhans\n'  # noqa: E501
    tag, value, trailing_modifier, comment = parse_tag_line(line)
    assert tag == "xref"
    assert value == "UMLS:C0022131"
    assert trailing_modifier == 'source="ncithesaurus:Islet_of_Langerhans"'
    assert comment == "Islets of Langerhans"


def test_parse_tag_line_backslashed_exclamation() -> None:
    line = "synonym: not a real example \\!\n"
    tag, value, trailing_modifier, comment = parse_tag_line(line)
    assert tag == "synonym"
    assert value == r"not a real example \!"


def test_parse_tag_line_curly_braces() -> None:
    """Test that we can handle curly braces inside tag lines"""
    line = 'synonym: "10*3.{copies}/mL" EXACT [] {http://purl.obolibrary.org/something="AB"}'
    tag, value, trailing_modifier, comment = parse_tag_line(line)
    assert tag == "synonym"
    assert value == '"10*3.{copies}/mL" EXACT []'
    assert trailing_modifier


def test_ignore_obsolete_nodes() -> None:
    """Quick verification that the change doesn't break anything"""
    path = os.path.join(directory, "data", "brenda-subset.obo")
    brenda = obonet.read_obo(path)
    nodes = brenda.nodes(data=True)
    assert "BTO:0000311" not in nodes


def test_presence_of_obsolete_nodes() -> None:
    """Test that we did, indeed, capture those obsolete entries"""
    pytest.importorskip("networkx", minversion="2.0")
    path = os.path.join(directory, "data", "brenda-subset.obo")
    brenda = obonet.read_obo(path, ignore_obsolete=False)
    nodes = brenda.nodes(data=True)
    assert "BTO:0000311" in nodes
    node = nodes["BTO:0000311"]
    assert node["is_obsolete"] == "true"
