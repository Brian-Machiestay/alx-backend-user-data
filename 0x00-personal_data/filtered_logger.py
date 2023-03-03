#!/usr/bin/env python3
"""filter and obfuscate user info"""
from typing import List
import re
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """filter user data"""
    m = message
    for field in fields:
        b = re.search(r'{}=.*'.format(field), m)
        assert b is not None
        m = re.sub(b.group().split(separator)[0],
                   '{}={}'.format(field, redaction), m)
    return m


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format the field"""
        record.msg = filter_datum(self.fields,
                                  RedactingFormatter.REDACTION,
                                  record.msg,
                                  RedactingFormatter.SEPARATOR)
        return super().format(record)
