#!/usr/bin/env python3
"""create session auth that expires"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """expiring session auth class"""
    user_id_by_session_id = {}

    def __init__(self):
        """the constructor method"""
        try:
            self.session_duration = int(os.environ['SESSION_DURATION'])
        except(Exception):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create an expiring session"""
        sess_id = super().create_session(user_id)
        if sess_id is None:
            return None
        sess_dict = {}
        sess_dict['user_id'] = user_id
        sess_dict['created_at'] = datetime.now()
        self.user_id_by_session_id[sess_id] = sess_dict
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """overload this function in parent"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        if not self.user_id_by_session_id[session_id]['created_at']:
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id]['user_id']
        create_at = self.user_id_by_session_id[session_id]['created_at']
        create_at_delta = timedelta(hours=create_at.hour,
                                    minutes=create_at.minute,
                                    seconds=create_at.second)
        sess_dura_delta = timedelta(seconds=self.session_duration)
        current = datetime.now()
        current_delta = timedelta(hours=current.hour,
                                  minutes=current.minute,
                                  seconds=current.second)
        if create_at_delta + sess_dura_delta < current_delta:
            return None
        return self.user_id_by_session_id[session_id]['user_id']
