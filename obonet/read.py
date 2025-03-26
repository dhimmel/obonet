from __future__ import annotations

import itertools
import logging
import re
from typing import Any, Iterator

import networkx

from .io import PathType, open_read_file

logger = logging.getLogger(__name__)


def read_obo(
    path_or_file: PathType, ignore_obsolete: bool = True, encoding: str | None = "utf-8"
) -> networkx.MultiDiGraph[str]:
    """
    Return a networkx.MultiDiGraph of the ontology serialized by the
    specified path or file.

    This function attempts to follow the specifications provided at:
    http://owlcollab.github.io/oboformat/doc/obo-syntax.html

    Parameters
    ==========
    path_or_file : str or file
        Path, URL, or open file object. If path or URL, compression is
        inferred from the file extension.
    ignore_obsolete : boolean
        When true (default), terms that are marked 'is_obsolete' will
        not be added to the graph.
    encoding : str or None
        The character set encoding to use for path_or_file when path_or_file
        is a path/URL. Set to None for platform-dependent locale default.
    """
    with open_read_file(path_or_file, encoding=encoding) as obo_file:
        typedefs, terms, instances, header = get_sections(obo_file)

    if "ontology" in header:
        header["name"] = header.get("ontology")
    if "name" not in header:
        logging.warning("name and ontology keys are both missing")
    graph = networkx.MultiDiGraph(typedefs=typedefs, instances=instances, **header)

    edge_tuples = []

    for term in terms:
        is_obsolete = term.get("is_obsolete", "false") == "true"
        if ignore_obsolete and is_obsolete:
            continue
        term_id = term.pop("id")
        graph.add_node(term_id, **term)

        for target_term in term.pop("is_a", []):
            edge_tuple = term_id, "is_a", target_term
            edge_tuples.append(edge_tuple)

        for relationship in term.pop("relationship", []):
            typedef, target_term = relationship.split(" ")
            edge_tuple = term_id, typedef, target_term
            edge_tuples.append(edge_tuple)

    for term0, typedef, term1 in edge_tuples:
        graph.add_edge(term0, term1, key=typedef)

    return graph


def get_sections(
    lines: Iterator[str],
) -> tuple[
    list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]
]:
    """
    Separates an obo file into stanzas and process.
    Returns (typedefs, terms, instances, header) tuples
    where `typedefs`, `terms`, and `instances` are lists of
    dictionaries and `header` is a dictionary.
    """
    typedefs, terms, instances = [], [], []
    header = None
    groups = itertools.groupby(lines, lambda line: line.strip() == "")
    for is_blank, stanza_lines_iter in groups:
        if is_blank:
            continue
        stanza_type_line, *stanza_lines = stanza_lines_iter
        if stanza_type_line.startswith("[Typedef]"):
            typedef = parse_stanza(stanza_lines, typedef_tag_singularity)
            typedefs.append(typedef)
        elif stanza_type_line.startswith("[Term]"):
            term = parse_stanza(stanza_lines, term_tag_singularity)
            terms.append(term)
        elif stanza_type_line.startswith("[Instance]"):
            instance = parse_stanza(stanza_lines, instance_tag_singularity)
            instances.append(instance)
        else:
            stanza_lines = [stanza_type_line] + stanza_lines
            header = parse_stanza(stanza_lines, header_tag_singularity)
    if header is None:
        logger.warning("got no header information")
        header = {}
    return typedefs, terms, instances, header


# regular expression to parse key-value pair lines.
tag_line_pattern = re.compile(
    r"""^
    (?P<tag>.+?):\s*             # tag and separator
    (?P<value>.*?)               # value: match anything (non-greedy)
    (?:\s                        # optional trailing modifier
        (?P<trailing_modifier>
            (?<!\\)\{[^{}]*\}    # match unescaped {...}
        )
    )?
    (?:\s
        (?P<comment>            # optional comment
            (?<!\\)![^\n]*      # match unescaped ! followed by any characters
        )
    )?
    \s*$                        # optional trailing whitespace
    """,
    re.VERBOSE,
)


def parse_tag_line(line: str) -> tuple[str, str | None, str | None, str | None]:
    """
    Take a line representing a single tag-value pair and parse
    the line into (tag, value, trailing_modifier, comment).
    """
    match = re.match(tag_line_pattern, line)
    if match is None:
        message = f"Tag-value pair parsing failed for:\n{line}"
        raise ValueError(message)
    tag = match.group("tag")
    value = match.group("value")
    trailing_modifier = match.group("trailing_modifier")
    if trailing_modifier:
        trailing_modifier = trailing_modifier.strip("{}")
    comment = match.group("comment")
    if comment:
        comment = comment.lstrip("! ")
    return tag, value, trailing_modifier, comment


def parse_stanza(lines: list[str], tag_singularity: dict[str, bool]) -> dict[str, Any]:
    """
    Returns a dictionary representation of a stanza.
    """
    stanza: dict[str, Any] = {}
    for line in lines:
        if line.startswith("!"):
            continue
        tag, value, trailing_modifier, comment = parse_tag_line(line)
        if tag_singularity.get(tag, False):
            stanza[tag] = value
        else:
            stanza.setdefault(tag, []).append(value)
    return stanza


header_tag_singularity = {
    "format-version": True,
    "data-version": True,
    "version": True,  # deprecated
    "ontology": True,
    "date": True,
    "saved-by": True,
    "auto-generated-by": True,
    "subsetdef": False,
    "import": False,
    "synonymtypedef": False,
    "idspace": False,
    "default-relationship-id-prefix": True,
    "id-mapping": False,
    "remark": False,
    # The following tags are new in OBO 1.4
    "treat-xrefs-as-equivalent": False,
    "treat-xrefs-as-genus-differentia": False,
    "treat-xrefs-as-relationship": False,
    "treat-xrefs-as-is_a": False,
    "relax-unique-identifier-assumption-for-namespace": False,
    "relax-unique-label-assumption-for-namespace": False,
}

term_tag_singularity = {
    "id": True,
    "is_anonymous": True,
    "name": True,
    "namespace": True,
    "alt_id": False,
    "def": True,
    "comment": True,
    "subset": False,
    "synonym": False,
    "exact_synonym": False,  # deprecated
    "narrow_synonym": False,  # deprecated
    "broad_synonym": False,  # deprecated
    "xref": False,
    "xref_unk": False,
    "is_a": False,
    "intersection_of": False,
    "union_of": False,
    "disjoint_from": False,
    "relationship": False,
    "is_obsolete": True,
    "replaced_by": False,
    "consider": False,
    "use_term": False,  # deprecated
    "builtin": True,
    # Additional tags in 1.4:
    "created_by": True,
    "creation_date": True,
}

typedef_tag_singularity = {
    "id": True,
    "is_anonymous": True,
    "name": True,
    "namespace": True,
    "alt_id": False,
    "def": True,
    "domain": True,
    "range": True,
    "inverse_of": False,
    "transitive_over": False,
    "is_cyclic": True,
    "is_reflexive": True,
    "is_symmetric": True,
    "is_anti_symmetric": True,
    "is_transitive": True,
    "is_metadata_tag": True,
    "is_class_level": True,
    # Additional tags in 1.4:
    "union_of": False,
    "intersection_of": False,
    "disjoint_from": False,
}

instance_tag_singularity = {
    "id": True,
    "is_anonymous": True,
    "name": True,
    "namespace": True,
    "alt_id": False,
    "def": False,
    "comment": True,
    "subset": False,
    "synonym": False,
    "xref": False,
    "instance_of": True,
    "property_value": False,
    "relationship": False,
    "created_by": True,
    "creation_date": True,
    "is_obsolete": True,
    "replaced_by": False,
    "consider": False,
}
