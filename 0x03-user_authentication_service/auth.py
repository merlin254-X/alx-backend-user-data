#!/usr/bin/env python3
"""
Auth module for user authentication.
"""
from db import DB
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid
from typing import Optional


def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string")
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """
    Generate a new UUID and return it as a string.
    This is a private method for internal use.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str):
        """
        Register a new user if the email is not already taken.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The newly created user object.

        Raises:
            ValueError: If the email is already taken.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except Exception:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate user credentials.
        Return True if email and password are correct, otherwise False.
        """
        try:
            user = self._db.find_user_by(email=email)
            if checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Optional[str]:
        """
        Create a new session ID for the user identified by the email.
        Returns the session ID or None if the user is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str):
        """Returns a user from the session_id or None if not found."""
        if session_id is None:
            return None

        try:
            # Query the database to find the user with the session_id
            user = self._db.session.query(User).filter_by(
                    session_id=session_id).one()
            return user
        except NoResultFound:
            # If no user found with the session_id, return None
            return None

    def destroy_session(self, user_id: str) -> None:
        """ Updates user's session_id to None"""
        if user_id is None:
            return None
        try:
            found_user = self._db.find_user_by(id=user_id)
            self._db.update_user(found_user.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ Finds user by email, updates user's reset_toke with UUID """
        try:
            found_user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(found_user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ Use the reset_token to find the corresponding user.
            If it does not exist, raise a ValueError exception.
        """
        if reset_token is None or password is None:
            return None

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=hashed_password,
                             reset_token=None)
