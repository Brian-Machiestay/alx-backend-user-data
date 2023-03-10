#!/usr/bin/env python3
"""create a session_auth class"""
from api.v1.auth.auth import Auth
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