#!/usr/bin/env python3
"""an Auth class to manage authentication"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """The authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """check the paths that require authentication
        """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        for pat in excluded_paths:
            if pat == path:
                return False
            if pat.startswith(path):
                return False
            ext = pat.find('*')
            if ext != -1:
                if path.startswith(pat[0:ext - 1]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """checks the authorizaton header
        """
        if request is None:
            return None
        if request.headers.get('Authorization', None) is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """checks the current user"""
        return None

    def session_cookie(self, request=None):
        """create a session cookie for storing session ids"""
        if request is None:
            return None
        if os.environ.get('SESSION_NAME') is not None:
            sess_name = os.environ['SESSION_NAME']
            return request.cookies.get(sess_name)
