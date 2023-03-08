#!/usr/bin/env python3
"""implement a basic authentication"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
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

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """extract user credentials"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if decoded_base64_authorization_header.find(':') == -1:
            return None, None
        credentials = decoded_base64_authorization_header.split(':')
        return credentials[0], credentials[1]

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """"return a user object based on email and password"""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        objs = User.search({'email': user_email})
        if objs is None or objs == []:
            return None
        actual_user = None
        for use in objs:
            if use.is_valid_password(user_pwd):
                actual_user = use
        return actual_user
