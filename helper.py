import math
from typing import TextIO, Iterable

_OVERLINE = "\u0305"


def write_to_file(data: Iterable[str], filename: str):
    with open(f"{filename}.html", "w", encoding="utf-8") as html_writer, open(
        f"{filename}.txt", "w", encoding="utf-8"
    ) as txt_writer:

        _write_html_header(html_writer)
        current_row = 0
        for line in data:
            current_row += 1
            _write_html_row(html_writer, current_row, line)
            _write_txt_line(txt_writer, line)

        _write_html_footer(html_writer)


def _write_html_header(writer: TextIO) -> None:
    writer.write("<html><body><table border='1'>\n")
    writer.write("<tr><th>No.</th><th>Bitstring</th><th>Value</th></tr>\n")


def _write_html_row(writer: TextIO, index: int, bitstring: str) -> None:
    html_bitstring = bitstring.replace(_OVERLINE, "&#773;")
    value = bitstring_value(bitstring)
    writer.write(
        f"<tr><td>{index}</td><td>{html_bitstring}</td><td>{value}</td></tr>\n"
    )


def _write_html_footer(writer: TextIO) -> None:
    writer.write("</table></body></html>\n")


def _write_txt_line(writer: TextIO, line: str):
    writer.write(line + "\n")


def bitstring_value(s: str) -> int:
    tokens = to_tokens(s)
    val = 0
    for i, token in enumerate(reversed(tokens)):
        if token[0] == "0":
            continue
        val += int(math.pow(2, i))
    return val


def to_tokens(s: str) -> list[str]:
    tokens: list[str] = []
    i = 0
    L = len(s)
    while i < L:
        ch = s[i]
        if i + 1 < L and s[i + 1] == _OVERLINE:
            tokens.append(ch + _OVERLINE)
            i += 2
        else:
            tokens.append(ch)
            i += 1
    return tokens


def tokens_to_str(tokens: list[str]) -> str:
    return "".join(tokens)


def overline(char: str) -> str:
    return char + _OVERLINE
