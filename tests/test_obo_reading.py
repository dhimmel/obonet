import os
import pathlib
from typing import Any

import pytest

import obonet
from obonet.read import parse_stanza, parse_tag_line, term_tag_singularity

directory = os.path.dirname(os.path.abspath(__file__))


def get_node(graph: Any, node: str) -> Any:
    if hasattr(graph, "node"):
        # NetworkX 1.x
        return graph.node[node]
    # NetworkX 2.x
    return graph.nodes[node]


def test_read_taxrank_file() -> None:
    """
    Test reading the taxrank ontology OBO file.
    """
    path = os.path.join(directory, "data", "taxrank.obo")
    with open(path) as read_file:
        taxrank = obonet.read_obo(read_file)
    assert len(taxrank) == 61
    assert get_node(taxrank, "TAXRANK:0000001")["name"] == "phylum"
    assert "NCBITaxon:kingdom" in get_node(taxrank, "TAXRANK:0000017")["xref"]


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
        tag_line = parse_tag_line(line)
        assert tag_line.tag == "saved-by"
        assert tag_line.value == "vw"
        assert tag_line.trailing_modifier is None
        assert tag_line.comment is None


def test_parse_tag_line_with_tag_and_value() -> None:
    line = 'synonym: "ovarian ring canal" NARROW []\n'
    tag_line = parse_tag_line(line)
    assert tag_line.tag == "synonym"
    assert tag_line.value == '"ovarian ring canal" NARROW []'
    assert tag_line.trailing_modifier is None
    assert tag_line.comment is None


def test_parse_tag_line_with_tag_value_and_comment() -> None:
    line = "is_a: GO:0005102 ! receptor binding\n"
    tag_line = parse_tag_line(line)
    assert tag_line.tag == "is_a"
    assert tag_line.value == "GO:0005102"
    assert tag_line.trailing_modifier is None
    assert tag_line.comment == "receptor binding"


def test_parse_tag_line_with_tag_value_and_trailing_modifier() -> None:
    line = 'xref: UMLS:C0226369 {source="ncithesaurus:Obturator_Artery"}\n'
    tag_line = parse_tag_line(line)
    assert tag_line.tag == "xref"
    assert tag_line.value == "UMLS:C0226369"
    assert tag_line.trailing_modifier == 'source="ncithesaurus:Obturator_Artery"'
    assert tag_line.comment is None


def test_parse_tag_line_with_tag_value_trailing_modifier_and_comment() -> None:
    line = 'xref: UMLS:C0022131 {source="ncithesaurus:Islet_of_Langerhans"} ! Islets of Langerhans\n'  # noqa: E501
    tag_line = parse_tag_line(line)
    assert tag_line.tag == "xref"
    assert tag_line.value == "UMLS:C0022131"
    assert tag_line.trailing_modifier == 'source="ncithesaurus:Islet_of_Langerhans"'
    assert tag_line.comment == "Islets of Langerhans"


def test_parse_tag_line_backslashed_exclamation() -> None:
    line = "synonym: not a real example \\!\n"
    tag_line = parse_tag_line(line)
    assert tag_line.tag == "synonym"
    assert tag_line.value == r"not a real example \!"


def test_parse_tag_line_curly_braces() -> None:
    """Test that we can handle curly braces inside tag lines"""
    line = 'synonym: "10*3.{copies}/mL" EXACT [] {http://purl.obolibrary.org/something="AB"}'
    tag_line = parse_tag_line(line)
    assert tag_line.tag == "synonym"
    assert tag_line.value == '"10*3.{copies}/mL" EXACT []'
    assert tag_line.trailing_modifier


def test_parse_stanza_with_clauses() -> None:
    lines = [
        'xref: DOID:14250 {source="MONDO:equivalentTo"} ! Down syndrome',
        'xref: GARD:0010247 {source="MONDO:equivalentTo"}',
        "xref: MESH:D004314 ! Down Syndrome",
        "xref: NCIT:C2993",
    ]
    stanza = parse_stanza(lines, term_tag_singularity, include_clauses=True)
    assert stanza["xref"] == [
        "DOID:14250",
        "GARD:0010247",
        "MESH:D004314",
        "NCIT:C2993",
    ]
    assert stanza["_clauses"] == [
        {
            "tag": "xref",
            "value": "DOID:14250",
            "trailing_modifier": 'source="MONDO:equivalentTo"',
            "comment": "Down syndrome",
        },
        {
            "tag": "xref",
            "value": "GARD:0010247",
            "trailing_modifier": 'source="MONDO:equivalentTo"',
            "comment": None,
        },
        {
            "tag": "xref",
            "value": "MESH:D004314",
            "trailing_modifier": None,
            "comment": "Down Syndrome",
        },
        {
            "tag": "xref",
            "value": "NCIT:C2993",
            "trailing_modifier": None,
            "comment": None,
        },
    ]


def test_read_obo_with_clauses() -> None:
    path = os.path.join(directory, "data", "taxrank.obo")
    taxrank = obonet.read_obo(path)
    node = get_node(taxrank, "TAXRANK:0000001")
    assert "_clauses" not in node

    taxrank = obonet.read_obo(path, include_clauses=True)
    node = get_node(taxrank, "TAXRANK:0000001")
    clauses = node["_clauses"]
    assert clauses[0] == {
        "tag": "id",
        "value": "TAXRANK:0000001",
        "trailing_modifier": None,
        "comment": None,
    }
    assert clauses[1] == {
        "tag": "name",
        "value": "phylum",
        "trailing_modifier": None,
        "comment": None,
    }


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
