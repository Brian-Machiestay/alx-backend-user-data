#!/usr/bin/env python3
"""filter and obfuscate user info"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """filter user data"""
    m = message
    for field in fields:
        b = re.search(r'{}=.*'.format(field), m)
        assert b is not None
        m = re.sub(b.group().split(';')[0],
                   '{}={}'.format(field, redaction), m)
    return m
