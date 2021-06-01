"""a minimalist (?) and simple ini parser. read-only. sections unsupported."""

import io
import re

from typing import Union

__version__ = "0.1.0"

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
_OPT_PTR = re.compile(rf"^\s*(?P<key>.*)\s*[{r'|'.join(DELIMITERS)}]\s*(?P<value>.*)\s*$")


class ParsingError(Exception):
    """parsing error base exception"""

    def __init__(self, msg, line, text=""):
        self.msg = msg
        self.line = line
        self.text = text

    def __str__(self):
        return f"{self.msg}, {self.text} [line: {self.line}]"


def get(string: Union[str, io.StringIO], key: str) -> str:
    """get option's value from string"""
    if type(string) is str:
        string = io.StringIO(string).readlines()
    elif type(string) is io.StringIO:
        string = string.readlines()
    else:
        TypeError("string must be either `StringIO` type or just `str`")

    for lineno, line in enumerate(string):
        lineno += 1

        if line.strip().startswith(tuple(COMMENT_PREFIX)) or not line.strip():
            continue

        opt = _OPT_PTR.match(line.strip())

        if opt:
            key_, val = opt.group("key", "value")

            if not key_.strip():
                raise ParsingError("key does not have a name", lineno, line.strip())

            if key == key_.strip():
                return val.strip()

        else:
            raise ParsingError("line contains parsing error", lineno, line.strip())


def getall(string: Union[io.StringIO, str]) -> dict:
    """get all option's value"""
    result = {}

    if type(string) is str:
        string = io.StringIO(string).readlines()
    elif type(string) is io.StringIO:
        string = string.readlines()
    else:
        TypeError("string must be either `StringIO` type or just `str`")

    for lineno, line in enumerate(string):
        lineno += 1

        if line.strip().startswith(tuple(COMMENT_PREFIX)) or not line.strip():
            continue

        opt = _OPT_PTR.match(line.strip())

        if opt:
            key, val = opt.group("key", "value")

            if not key.strip():
                raise ParsingError("key does not have a name", lineno, line.strip())

            if key.strip() not in result:
                result.update({key.strip(): val.strip()})
            else:
                raise ParsingError(
                    f"option with key `{key}` already exists", lineno, line.strip()
                )
        else:
            raise ParsingError("line contains parsing error", lineno, line.strip())

    return result


def getint(string: Union[io.StringIO, str], key: str) -> int:
    """get option's value in `int` type"""
    val = get(string, key)
    if val:
        return int(val)


def getfloat(string: Union[io.StringIO, str], key: str) -> float:
    """get option's value in `float` type"""
    val = get(string, key)
    if val:
        return float(val)


def getbool(string: Union[io.StringIO, str], key: str) -> bool:
    """get option's value in `bool` type"""
    val = get(string, key)
    if val:
        if val.lower() in BOOL_STATES:
            return BOOL_STATES[val]
        else:
            raise ValueError(f"unknown boolean states, {val}")
