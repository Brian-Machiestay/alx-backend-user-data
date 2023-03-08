#!/usr/bin/env python3
"""implement a basic authentication"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """A basic auth that inherits from auth"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """return the base64 str of the auth header"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """decode base64 string"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            str64 = base64.b64decode(base64_authorization_header)
            return str64.decode('utf-8')
        except(Exception):
            return None
