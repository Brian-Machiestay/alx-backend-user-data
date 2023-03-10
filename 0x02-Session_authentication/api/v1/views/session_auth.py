#!/usr/bin/env python3
"""a view function to query using session auth"""
from api.v1.views import app_views
from flask import abort, jsonify, request
import os
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """login using session auth"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400
    objs = User.search({'email': email})
    if objs is None or objs == []:
        return jsonify({"error": "no user found for this email"}), 404
    actual_user = None
    for use in objs:
        if use.is_valid_password(password):
            actual_user = use
    if actual_user is None:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    from api.v1.auth.session_auth import SessionAuth
    if os.environ['AUTH_TYPE'] == 'session_auth':
        auth = SessionAuth()
    sess_id = auth.create_session(actual_user.id)
    resp = jsonify(actual_user.to_json())
    cookie_name = os.environ['SESSION_NAME']
    resp.set_cookie(cookie_name, sess_id)
    return resp


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """logout of this session"""
    from api.v1.app import auth
    from api.v1.auth.session_auth import SessionAuth
    if os.environ['AUTH_TYPE'] == 'session_auth':
        auth = SessionAuth()
    des = auth.destroy_session(request)
    if not des:
        abort(404)
    return jsonify({}), 200
