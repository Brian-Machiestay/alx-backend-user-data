#!/usr/bin/env python3
"""python flask app defines routes to this application"""


from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
