#!/usr/bin/env python3
"""create a session_auth class"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """the auth class to handle session authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """function to create a session"""
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        session_id = uuid.uuid4()
        self.user_id_by_session_id[str(session_id)] = user_id
        return str(session_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """function to get user_id based on session id"""
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None
        usr_id = self.user_id_by_session_id.get(session_id)
        return usr_id

    def current_user(self, request=None):
        """return a user instance based on cookie value"""
        sess_id = self.session_cookie(request)
        usr_id = self.user_id_for_session_id(sess_id)
        if usr_id is not None:
            return User.get(usr_id)

    def destroy_session(self, request=None):
        """logout of this session"""
        if request is None:
            return False
        sess_id = self.session_cookie(request)
        if self.user_id_for_session_id(sess_id) is None:
            return False
        del self.user_id_by_session_id[sess_id]
        return True
