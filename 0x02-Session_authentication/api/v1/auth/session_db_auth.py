#!/usr/bin/env python3
"""create a session auth that saves to db"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """session authentication implementation"""

    def create_session(self, user_id=None):
        """create a session in db"""
        sess_id = super().create_session(user_id)
        if sess_id is None:
            return None
        usr_sess = UserSession(user_id)
        usr_sess.session_id = sess_id
        usr_sess.save()
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """overload the usr id for sess id method"""
        usr = UserSession.get(session_id)
        return usr

    def destroy_session(self, request=None):
        """destroy a session"""
        sess_id = self.session_cookie(request)
        usr_sess = UserSession.get(session_id)
        if usr_sess is not None:
            usr_sess.remove()
