"""a minimalist (?) and simple ini parser."""

import io

__version__ = "1.2.0"

COMMENT_PREFIX = ";#"
DELIMITERS = ("=", ":")


class ParsingError(Exception):
    """parsing error base exception"""

    def __init__(self, msg: str, line: int, text: str | None = ""):
        self.msg = msg
        self.line = line
        self.text = text
        super().__init__(self.msg)

    def __str__(self):
        return f"{self.msg}, {self.text} [line: {self.line}]"


def _strip_comment(text: str) -> str | None:
    """parse inline comment"""
    result = ""

    for char in text:
        if char in COMMENT_PREFIX:
            break

        result += char

    return result


def _parse_section(text: str) -> str | None:
    """parse section"""
    header = None

    if text[0] != "[":
        return header

    tokens = text.split("[", 1)
    tokens = tokens[1].split("]", 1)
    if len(tokens) == 2:
        header = tokens[0]

    return header


def _parse_option(text: str) -> tuple | None:
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

        key = tokens[0].strip()

    return (key, val)


def read(string: str | io.StringIO) -> dict:
    """read ini from string"""
    if not isinstance(string, (str, io.StringIO)):
        raise TypeError("`string` must be either StringIO object or just str")

    result = {}
    string = (
        string.readlines()
        if isinstance(string, io.StringIO)
        else io.StringIO(string).readlines()
    )
    prev_section = None
    prev_option = (None, None)

    for lineno, line in enumerate(string):
        lineno += 1
        sline = _strip_comment(line.strip())

        if not sline or sline[0] in COMMENT_PREFIX:
            continue

        section = _parse_section(sline)

        if section:
            prev_section = section
            result.update({section: {}})
        else:
            if sline[0] == "[" or sline[-1] == "]":
                raise ParsingError("Error parsing section", lineno, line)

            option = _parse_option(sline)

            if not option[0]:
                raise ParsingError("Error parsing option without a name", lineno, line)

            if (
                option[1] is None
                and line[0] in " \t\n"
                and prev_option[0]
                and prev_option[1] is not None
            ):
                target = result[prev_section] if prev_section else result
                target[prev_option[0]] += (
                    sline if not target[prev_option[0]] else f"\n{sline}"
                )
                continue

            if prev_section:
                if option[0] in result[prev_section]:
                    raise ParsingError(
                        f"option `{option[0]}` already exists", lineno, line
                    )

                result[prev_section].update({option[0]: option[1]})
            else:
                if option[0] in result:
                    raise ParsingError(
                        f"option `{option[0]}` already exists", lineno, line
                    )

                result.update({option[0]: option[1]})

            prev_option = option

    return result


def write(data: dict, file: str):
    """write ini to file, this will remove comments"""
    with open(file, "w", encoding="UTF-8") as fctx:
        result = ""

        for sec in data:
            if isinstance(data[sec], dict):
                result += f"[{sec}]\n" if not result else f"\n[{sec}]\n"
                for secopt in data[sec]:
                    value = str(data[sec][secopt]) if data[sec][secopt] else None

                    if value:
                        result += f"{secopt} = " + value.split("\n", 2)[0] + "\n"
                    else:
                        result += f"{secopt}\n"

                    if value:
                        for optl in value.split("\n")[1:]:
                            result += f"\t{optl}\n"
            else:
                value = str(data[sec]) if data[sec] else None

                if value:
                    result += f"{sec} = " + value.split("\n", 2)[0] + "\n"
                else:
                    result += f"{sec}\n"

                if value:
                    for optl in value.split("\n")[1:]:
                        result += f"\t{optl}\n"

        fctx.write(result)
