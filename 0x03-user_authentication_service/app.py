#!/usr/bin/env python3
"""python flask app defines routes to this application"""


from flask import Flask, jsonify, request, abort, make_response
from flask import redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def root():
    """return the homepage of this application"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """register a user on this application"""
    email = request.form.get('email', None)
    pwd = request.form.get('password', None)
    try:
        usr = AUTH.register_user(email, pwd)
        return jsonify({"email": usr.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """log this user in using the session"""
    email = request.form.get('email', None)
    pwd = request.form.get('password', None)
    correct_details = AUTH.valid_login(email, pwd)
    if not correct_details:
        abort(401)
    sess_id = AUTH.create_session(email)
    resp = make_response(jsonify({"email": email, "message": "logged in"}))
    resp.set_cookie("session_id", sess_id)
    return resp


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """log this user out of the the session"""
    sess_id = request.cookie.get('session_id')
    usr = AUTH.get_user_from_session_id(sess_id)
    if usr is not None:
        AUTH.destroy_session(usr.id)
        return redirect(url_for('root'))
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
