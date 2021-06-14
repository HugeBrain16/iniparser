import iniparser

def test_read():
	text = """
	name = joe
	who = joe mama
	joe mama = not funni
	"""

	data = iniparser.getall(text)

	assert "name" in data
	assert "who" in data
	assert "joe mama" in data

	assert data["name"] == "joe"
	assert data["who"] == "joe mama"
	assert data["joe mama"] == "not funni"

def test_conv():
	text = """
	rat = 3
	size = 8.0
	cockroach = false
	"""

	rat = iniparser.getint(text, "rat")
	size = iniparser.getfloat(text, "size")
	cockroach = iniparser.getbool(text, "cockroach")

	assert type(rat) is int
	assert type(size) is float
	assert type(cockroach) is bool

def test_section():
	text = """
	[main]
	name = sven
	age = 22
	"""

	assert iniparser.get(text, "name", "main") == "sven"
	assert iniparser.getint(text, "age", "main") == 22
