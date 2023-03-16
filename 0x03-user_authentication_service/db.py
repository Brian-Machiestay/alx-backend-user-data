#!/usr/bin/env python3
"""DB module
"""


from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from user import User  # type: ignore
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base  # type: ignore


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add a user to the database"""
        usr = User(email=email, hashed_password=hashed_password)
        self._session.add(usr)
        self._session.commit()
        return usr

    def find_user_by(self, **kwargs) -> User:
        """filter user by key worded arguments"""
        objs = self._session.query(User).filter_by(**kwargs).first()
        if objs is None:
            raise NoResultFound
        return objs

    def update_user(self, user_id: int, **kwargs) -> None:
        """update a user data in the database"""
        usr = self.find_user_by(id=user_id)
        for key in kwargs.keys():
            if key not in usr.__dict__.keys():
                raise ValueError
            setattr(usr, key, kwargs[key])
        self._session.commit()
