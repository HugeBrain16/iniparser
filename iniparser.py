"""a minimalist (?) and simple ini parser."""

import io

from typing import Union
from typing import Optional
from typing import Any

__version__ = "1.0.0"

BOOL_STATES = {
    "false": False,
    "0": False,
    "off": False,
    "no": False,
    "true": True,
    "1": True,
    "on": True,
    "yes": True,
}
COMMENT_PREFIX = ";#"
DELIMITERS = ("=", ":")


class ParsingError(Exception):
    """parsing error base exception"""

    def __init__(self, msg: str, line: int, text: Optional[str] = ""):
        self.msg = msg
        self.line = line
        self.text = text
        super().__init__(self.msg)

    def __str__(self):
        return f"{self.msg}, {self.text} [line: {self.line}]"


def _parse_inline_comment(text: str) -> Union[str, None]:
    """parse inline comment"""
    result = text

    cmt = text.split(" ", 1)
    if len(cmt) == 2:
        rest = cmt[1].strip()

        if rest[0] in COMMENT_PREFIX:
            result = cmt[0]

    return result


def _parse_section(text: str) -> Union[str, None]:
    """parse section"""
    header = None

    if text[0] != "[":
        return header

    tokens = text.split("[", 1)
    tokens = tokens[1].split("]", 1)
    if len(tokens) == 2:
        header = tokens[0]

        if tokens[1] and tokens[1].strip()[0] not in COMMENT_PREFIX:
            header = None

    if header:
        cmt_header = header.split(" ", 1)
        if len(cmt_header) == 2:
            rest = cmt_header[1].strip()

            if rest[0] in COMMENT_PREFIX:
                header = None

    return header


def _parse_option(text: str) -> Union[tuple, None]:
    """parse option"""
    key = None
    val = None

    if not text:
        return None

    for delim in DELIMITERS:
        tokens = text.split(delim, 1)

        if len(tokens) == 2:
            key = tokens[0].strip()
            val = tokens[1].strip()
            break

        elif len(tokens) < 2:
            key = tokens[0].strip()

    cmt_key = key.split(" ", 1)
    if len(cmt_key) == 2:
        rest = cmt_key[1].strip()

        if rest[0] in COMMENT_PREFIX:
            key = cmt_key[0]
            val = None

    if val:
        cmt_val = val.split(" ", 1)
        if len(cmt_val) == 2:
            rest = cmt_val[1].strip()

            if rest[0] in COMMENT_PREFIX:
                val = cmt_val[0]

    return (key, val)


def get(
    string: Union[str, io.StringIO], key: str, section: Optional[str] = None
) -> Union[str, None]:
    """get option's value from string"""
    data = getall(string)

    if section:
        return data[section][key]

    return data[key]


def getall(string: Union[str, io.StringIO]) -> tuple:
    """get all sections and options from string"""
    result = {}

    if isinstance(string, str):
        string = io.StringIO(string).readlines()
    elif isinstance(string, io.StringIO):
        string = string.readlines()
    else:
        raise TypeError("`string` must be either StringIO object or just str")

    prev_section = None
    prev_option = None

    for lineno, line in enumerate(string):
        lineno += 1
        line = line.strip()

        if not line:
            continue

        if line[0] in COMMENT_PREFIX:
            continue

        section = _parse_section(line)

        if section:
            prev_section = section
            result.update({section: {}})
        else:
            option = _parse_option(line)

            prev_option = option

            if prev_section:
                if option[0] not in result[prev_section]:
                    result[prev_section].update({option[0]: option[1]})
                else:
                    raise ParsingError(
                        f"option `{option[0]}` already exists", lineno, line
                    )
            else:
                if option[0] not in result:
                    result.update({option[0]: option[1]})
                else:
                    raise ParsingError(
                        f"option `{option[0]}` already exists", lineno, line
                    )

    return result


def getint(
    string: Union[io.StringIO, str], key: str, section: Optional[str] = None
) -> Union[int, None]:
    """get option's value in `int` type"""
    val = get(string, key, section)
    if val:
        return int(val)


def getfloat(
    string: Union[io.StringIO, str], key: str, section: Optional[str] = None
) -> Union[float, None]:
    """get option's value in `float` type"""
    val = get(string, key, section)
    if val:
        return float(val)


def getbool(
    string: Union[io.StringIO, str], key: str, section: Optional[str] = None
) -> Union[bool, None]:
    """get option's value in `bool` type"""
    val = get(string, key, section)
    if val:
        if val.lower() in BOOL_STATES:
            return BOOL_STATES[val]

        raise ValueError(f"unknown boolean states, {val}")


def fget(
    file: Union[io.TextIOWrapper, str], key: str, section: Optional[str] = None
) -> Union[str, None]:
    """get option's value from file"""
    if isinstance(file, io.TextIOWrapper):
        value = get(file.read(), key, section)
    elif isinstance(file, str):
        value = get(open(file, "r", encoding="UTF-8").read(), key, section)

    return value


def fgetint(
    file: Union[io.TextIOWrapper, str], key: str, section: Optional[str] = None
) -> Union[int, None]:
    """get option's value in `int` type from file"""
    val = fget(file, key, section)
    if val:
        return int(val)


def fgetint(
    file: Union[io.TextIOWrapper, str], key: str, section: Optional[str] = None
) -> Union[float, None]:
    """get option's value in `float` type from file"""
    val = fget(file, key, section)
    if val:
        return float(val)


def fgetbool(
    file: Union[io.TextIOWrapper, str], key: str, section: Optional[str] = None
) -> Union[bool, None]:
    """get option's value in `bool` type from file"""
    val = fget(file, key, section)
    if val:
        if val.lower() in BOOL_STATES:
            return BOOL_STATES[val]

        raise ValueError(f"unknown boolean states, {val}")
