import io
import re
import inspect
import functools
from bisect import bisect
from tokenize import tokenize, untokenize
from token import tok_name

RE_TEMPLATE = re.compile(rb"(?:{{|}}|[^{}])*(?={|$)")


class ParseError(ValueError):
    pass


def split(string):
    data = string.encode("utf-8")
    bio = io.BytesIO(data)

    row_offsets = [0]
    for line in data.split(b"\n"):
        row_offsets.append(row_offsets[-1] + len(line) + 1)

    strings = []
    exprs = []
    start = 0
    while True:
        match = RE_TEMPLATE.match(data, start)
        if not match:
            raise ParseError("unbalanced closing braces")
        strings.append(
            match.group(0).replace(b"{{", b"{").replace(b"}}", b"}").decode("utf-8")
        )
        start = match.end()
        if start == len(data):
            break

        start += 1
        bio.seek(start)

        expr, row, column = parse_expr(bio)
        exprs.append(compile(expr, "", "eval"))

        start_row = bisect(row_offsets, start) - 1
        if row > 0:
            start = row_offsets[row + start_row] + column
        else:
            start = start + column

    return tuple(strings), tuple(exprs)


def parse_expr(bio):
    count = 0
    tokens = []
    for t in tokenize(bio.readline):
        if tok_name[t[0]] == "OP":
            if t[1] == "{":
                count += 1
            elif t[1] == "}":
                if count == 0:
                    row, column = t[3]
                    return untokenize(tokens).decode("utf-8"), row - 1, column
                count -= 1
        tokens.append(t)
    raise ParseError("unterminated expression")


def tag(func=None, *, cache_maxsize=128):
    cached_split = functools.lru_cache(cache_maxsize)(split)

    def _tag(func):
        @functools.wraps(func)
        def __tag(string):
            strings, exprs = cached_split(string)

            stack = inspect.stack()
            f_globals = stack[1].frame.f_globals
            f_locals = stack[1].frame.f_locals
            del stack

            values = []
            for expr in exprs:
                values.append(eval(expr, f_globals, f_locals))
            return func(strings, tuple(values))
        return __tag

    if func:
        return _tag(func)
    return _tag


__all__ = ["tag", "ParseError"]
