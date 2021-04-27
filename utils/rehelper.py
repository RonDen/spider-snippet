import re


_pattern = re.compile(r'\d+')


def reg_int(s: str):
    res = _pattern.search(s)
    return int(res.group(0))
