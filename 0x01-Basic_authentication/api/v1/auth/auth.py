#!/usr/bin/env python3
"""
Auth module for API authentication
"""
from typing import List, TypeVar
from flask import request

class Auth:
    """Auth class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to determine if authentication is required
        Returns True if path is None or not in excluded_paths
        """
        if path is None:
            return True

        if not excluded_paths or len(excluded_paths) == 0:
            return True

        # Normalize the path to end with a slash for comparison
        if not path.endswith('/'):
            path += '/'

        # Check if the normalized path is in the list of excluded paths
        for excluded_path in excluded_paths:
            if excluded_path.endswith('/') and path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Method to get the Authorization header from the request
        Returns None for now
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method to get the current user
        Returns None for now
        """
        return None
