#!/usr/bin/env python3
"""SessionAuth module"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """ Session Authentication """

    # Class attribute initialized as an empty dictionary
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for the given user_id.

        Args:
            user_id (str): The user ID to create a session for.

        Returns:
            str: The session ID or None if user_id is invalid.
        """
        # Validate user_id
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a new session ID using uuid4
        session_id = str(uuid.uuid4())

        # Store the user_id in the dictionary with session_id as key
        self.user_id_by_session_id[session_id] = user_id

        # Return the session ID
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns User ID based on Session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The user ID if found, otherwise None.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        # Retrieve user_id from the session ID dictionary
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a User instance based on cookie value.

        Args:
            request: The Flask request object.

        Returns:
            User: User instance if session is valid, otherwise None.
        """
        # Retrieve session ID from the request cookie
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        # Retrieve user ID from the session ID
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        # Retrieve and return the User instance from the database
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ Deletes user session to logout """

        if request is None:
            return False
        cookie = self.session_cookie(request)
        if cookie is None or self.user_id_for_session_id(cookie) is None:
            return False
        del self.user_id_by_session_id[cookie]
        return True
