#!/usr/bin/env python3
"""main file"""


from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()
usr = auth.register_user(email, password)
print(auth.create_session(email))
print(usr.session_id)
auth.destroy_session(usr.id)
print(usr.session_id)
