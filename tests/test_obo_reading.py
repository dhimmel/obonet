import pytest

def test_parse_tag_line_newline_agnostic():
    import obo.read
    for line in ['saved-by: vw', 'saved-by: vw\n']:
        tag, value, trailing_modifier, comment = obo.read.parse_tag_line(line)
        assert tag == 'saved-by'
        assert value == 'vw'
        assert trailing_modifier == None
        assert comment == None

def test_parse_tag_line_with_tag_and_value():
    import obo.read
    line = 'synonym: "ovarian ring canal" NARROW []\n'
    tag, value, trailing_modifier, comment = obo.read.parse_tag_line(line)
    assert tag == 'synonym'
    assert value == '"ovarian ring canal" NARROW []'
    assert trailing_modifier == None
    assert comment == None

def test_parse_tag_line_with_tag_value_and_comment():
    import obo.read
    line = "is_a: GO:0005102 ! receptor binding\n"
    tag, value, trailing_modifier, comment = obo.read.parse_tag_line(line)
    assert tag == 'is_a'
    assert value == 'GO:0005102'
    assert trailing_modifier == None
    assert comment == 'receptor binding'

def test_parse_tag_line_with_tag_value_and_trailing_modifier():
    import obo.read
    line = 'xref: UMLS:C0226369 {source="ncithesaurus:Obturator_Artery"}\n'
    tag, value, trailing_modifier, comment = obo.read.parse_tag_line(line)
    assert tag == 'xref'
    assert value == 'UMLS:C0226369'
    assert trailing_modifier == 'source="ncithesaurus:Obturator_Artery"'
    assert comment == None

def test_parse_tag_line_with_tag_value_trailing_modifier_and_comment():
    import obo.read
    line = 'xref: UMLS:C0022131 {source="ncithesaurus:Islet_of_Langerhans"} ! Islets of Langerhans\n'
    tag, value, trailing_modifier, comment = obo.read.parse_tag_line(line)
    assert tag == 'xref'
    assert value == 'UMLS:C0022131'
    assert trailing_modifier == 'source="ncithesaurus:Islet_of_Langerhans"'
    assert comment == 'Islets of Langerhans'

if __name__ == '__main__':
    pytest.main()
