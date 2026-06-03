import os
import pathlib
from typing import Any

from obonet.cli import main

directory = os.path.dirname(os.path.abspath(__file__))


def test_cli_stdout(capsys: Any) -> None:
    path = os.path.join(directory, "data", "taxrank.obo")
    main([path, "--include-clauses"])
    captured = capsys.readouterr()
    assert '"directed": true' in captured.out
    assert '"multigraph": true' in captured.out
    assert '"TAXRANK:0000060"' in captured.out
    assert '"taxonomic_rank"' in captured.out


def test_cli_output_file(tmp_path: pathlib.Path) -> None:
    path = os.path.join(directory, "data", "taxrank.obo")
    output = tmp_path / "taxrank.json"
    main([path, "--output", str(output), "--indent", "0"])
    text = output.read_text()
    assert '"directed": true' in text
    assert '"TAXRANK:0000060"' in text
    assert '"_clauses"' not in text
