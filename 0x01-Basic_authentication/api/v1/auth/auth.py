#!/usr/bin/env python3
"""Auth class for managing API authentication."""
from typing import List, TypeVar
from flask import request


class Auth:
    """Auth class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if a path requires authentication.
        """

        if path is None or not excluded_paths:
            return True

        # Normalize path by ensuring it ends with a '/'
        if not path.endswith('/'):
            path += '/'

        # Check if the path is in excluded_paths
        for exclusion in excluded_paths:
            if exclusion.endswith('/') and path == exclusion:
                return False
            if path == exclusion.rstrip('/'):
                return False
        
        return True

    def authorization_header(self, request=None) -> str:
        """Gets the authorization header from a request.
        """

        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user (to be implemented later).

        Args:
            request (Flask request): The request object.

        Returns:
            TypeVar('User'): None, as it will be implemented later.
        """
        return None
