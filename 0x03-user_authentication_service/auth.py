#!/usr/bin/env python3
"""implement an authentication system"""


import bcrypt
from base64 import standard_b64encode


def _hash_password(password: str) -> bytes:
    """"implement a method that returns bytes password"""
    pwd = password.encode('utf-8')
    return bcrypt.hashpw(pwd, bcrypt.gensalt())
