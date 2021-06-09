"""a minimalist (?) and simple ini parser. sections unsupported."""

import io
import re

from typing import Union
from typing import Optional
from typing import Any

__version__ = "0.3.0"

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
_OPT_PTR = re.compile(rf"^\s*(?P<key>.*)\s*[{''.join(DELIMITERS)}]\s*(?P<value>.*)\s*$")


class ParsingError(Exception):
    """parsing error base exception"""

    def __init__(self, msg: str, line: int, text: Optional[str] = ""):
        self.msg = msg
        self.line = line
        self.text = text
        super().__init__(self.msg)

    def __str__(self):
        return f"{self.msg}, {self.text} [line: {self.line}]"


def get(string: Union[str, io.StringIO], key: str) -> Union[str, None]:
    """get option's value from string"""
    if isinstance(string, str):
        string = io.StringIO(string).readlines()
    elif isinstance(string, io.StringIO):
        string = string.readlines()
    else:
        raise TypeError("string must be either `StringIO` type or just `str`")

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

    if isinstance(string, str):
        string = io.StringIO(string).readlines()
    elif isinstance(string, io.StringIO):
        string = string.readlines()
    else:
        raise TypeError("string must be either `StringIO` type or just `str`")

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


def getint(string: Union[io.StringIO, str], key: str) -> Union[int, None]:
    """get option's value in `int` type"""
    val = get(string, key)
    if val:
        return int(val)


def getfloat(string: Union[io.StringIO, str], key: str) -> Union[float, None]:
    """get option's value in `float` type"""
    val = get(string, key)
    if val:
        return float(val)


def getbool(string: Union[io.StringIO, str], key: str) -> Union[bool, None]:
    """get option's value in `bool` type"""
    val = get(string, key)
    if val:
        if val.lower() in BOOL_STATES:
            return BOOL_STATES[val]

        raise ValueError(f"unknown boolean states, {val}")


def fget(file: Union[io.TextIOWrapper, str], key: str) -> Union[str, None]:
    """get option's value from file"""
    if isinstance(file, io.TextIOWrapper):
        value = get(file.read(), key)
    elif isinstance(file, str):
        value = get(open(file, "r", encoding="UTF-8").read(), key)

    return value


def fgetint(file: Union[io.TextIOWrapper, str], key: str) -> Union[int, None]:
    """get option's value in `int` type from file"""
    val = fget(file, key)
    if val:
        return int(val)


def fgetint(file: Union[io.TextIOWrapper, str], key: str) -> Union[float, None]:
    """get option's value in `float` type from file"""
    val = fget(file, key)
    if val:
        return float(val)


def fgetbool(file: Union[io.TextIOWrapper, str], key: str) -> Union[bool, None]:
    """get option's value in `bool` type from file"""
    val = fget(file, key)
    if val:
        if val.lower() in BOOL_STATES:
            return BOOL_STATES[val]

        raise ValueError(f"unknown boolean states, {val}")


def set(string: Union[io.StringIO, str], key: str, value: Any) -> str:
    """set new option to string, return string with new option"""
    opts = getall(string)
    opts.update({key: value})

    return "\n".join([key + " = " + opts[key] for key in opts])


def fset(file: Union[io.TextIOWrapper, str], key: str, value: Any) -> None:
    """set new option to file"""
    if isinstance(file, io.TextIOWrapper):
        data = set(file.read(), key, value)
        open(file.name, "w", encoding="UTF-8").write(data)
    elif isinstance(file, str):
        data = set(open(file, "r", encoding="UTF-8").read(), key, value)
        open(file, "w", encoding="UTF-8").write(data)
