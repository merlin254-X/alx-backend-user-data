#!/usr/bin/env python3
"""
DB module.
"""
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DB:
    """DB class for managing database operations."""

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created user object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by arbitrary attributes.

        Args:
            **kwargs: Arbitrary keyword arguments for filtering the query.

        Returns:
            User: The first user that matches the filter criteria.

        Raises:
            NoResultFound: If no user matches the filter criteria.
            InvalidRequestError: If the filter criteria are invalid.
        """
        if not kwargs:
            raise InvalidRequestError("No arguments provided for query.")
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound("No user found with the provided attributes.")
        except InvalidRequestError as e:
            raise InvalidRequestError(f"Invalid query arguments: {e}")

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes in the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Key-value pairs of attributes to update.

        Returns:
            None

        Raises:
            ValueError: If any of the attributes in kwargs do not exist.
        """
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Attribute {key} does not exist on User.")
            setattr(user, key, value)

        self._session.commit()
