#!/usr/bin/env python3
"""model for session saved in database"""

from models.base import Base


class UserSession(Base):
    """implements a user session model"""

    def __init__(self, *args: list, **kwargs: dict):
        """initialize an instance of this class"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
