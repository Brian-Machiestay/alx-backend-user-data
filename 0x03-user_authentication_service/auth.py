#!/usr/bin/env python3
"""implement an authentication system"""


import bcrypt
from base64 import standard_b64encode
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """"implement a method that returns bytes password"""
    pwd = password.encode('utf-8')
    return bcrypt.hashpw(pwd, bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """add a user into the database"""
        try:
            usr = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(usr.email))
        except NoResultFound:
            pwd = _hash_password(password)
            user = self._db.add_user(email, pwd)
            return user
