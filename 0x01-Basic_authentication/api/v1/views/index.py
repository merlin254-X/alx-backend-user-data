#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """

@app_views.route('/unauthorized/', strict_slashes=False)
def unauthorized() -> None:
    """ Endpoint to trigger a 401 Unauthorized error """
    abort(401)

@app_views.route('/forbidden/', strict_slashes=False)
def forbidden() -> None:
    """ Endpoint to trigger a 403 Forbidden error """
    abort(403)

    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)
