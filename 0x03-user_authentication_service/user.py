#!/usr/bin/env python3
"""the user class to manage authentication service"""


from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy import Column, Integer, String # type: ignore


Base = declarative_base()


class User(Base): # type: ignore
    """A user class subclasses the declarative base"""

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))
