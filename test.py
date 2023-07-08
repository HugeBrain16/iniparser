import iniparser


def test_read():
    text = """
	opt1 = val
	opt2 = val with space1
	opt with space = val with space2
	"""

    data = iniparser.read(text)

    assert data["opt1"] == "val"
    assert data["opt2"] == "val with space1"
    assert data["opt with space"] == "val with space2"


def test_section():
    text = """
	[main]
	opt1 = val1

    [main with space]
    opt1 = val1
	"""

    data = iniparser.read(text)

    assert data["main"]["opt1"] == "val1"
    assert data["main with space"]["opt1"] == "val1"


def test_multiline():
    text = """
    header
header1
    header2
content =
    fake1
    fake2

[main]
test = asdf
    wasd
secheader

content1 =
 [main1]
    """

    data = iniparser.read(text)

    assert all(data[header] is None for header in ("header", "header1", "header2"))
    assert data["main"]["secheader"] is None
    assert data["content"] == "fake1\nfake2"
    assert data["main"]["test"] == "asdf\nwasd"
    assert data["main"]["content1"] != "[main1]"
