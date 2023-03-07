#!/usr/bin/env python3
"""an Auth class to manage authentication"""
from flask import request
from typing import List, TypeVar


class Auth:
    """The authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """check the paths that require authentication"""
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        for pat in excluded_paths:
            if pat == path:
                return False
            if pat.startswith(path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """checks the authorizaton header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """checks the current user"""
        return None
