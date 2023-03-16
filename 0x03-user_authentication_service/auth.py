#!/usr/bin/env python3
"""implement an authentication system"""


import bcrypt
from base64 import standard_b64encode
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """"implement a method that returns bytes password"""
    pwd = password.encode('utf-8')
    return bcrypt.hashpw(pwd, bcrypt.gensalt())


def _generate_uuid() -> str:
    """generate uuid and return a str repr"""
    uid = uuid4()
    return str(uid)


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

    def valid_login(self, email: str, password: str) -> bool:
        """check that this user is valid"""
        try:
            usr = self._db.find_user_by(email=email)
            pwd = password.encode('utf-8')
            return bcrypt.checkpw(pwd, usr.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """create and return a session id for this user"""
        try:
            usr = self._db.find_user_by(email=email)
            sess_id = _generate_uuid()
            self._db.update_user(usr.id, session_id=sess_id)
            return sess_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """get the user by session id"""
        try:
            usr = self._db.find_user_by(session_id=session_id)
            return usr
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroy the session id for this user"""
        try:
            usr = self._db.find_user_by(id=user_id)
            self._db.update_user(self, user_id, session_id=None)
            return None
        except NoResultFound:
            return None
