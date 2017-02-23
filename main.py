#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

header = "<h1>User Signup</h1>"

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

def writeForm(name, email, ue, pe, ve, ee):
    user = "<label>Username: </label><input type='text' name='username' value=" + name + ">" + ue
    passw = "<label>Password: </label><input type='password' name='password' value=''>" + pe
    validp = "<label>Verify Password: </label><input type='password' name='verify' value=''>" + ve
    email = "<label>Email (Optional): </label><input type='text' name='email' value=" + email + ">" + ee
    submit = "<input type='submit'>" "</input>"
    form = "<form method='post'>" + user + "<br>" + passw + "<br>" + validp + "<br>" + email + "<br>" + submit + "</form>"
    return form

class MainHandler(webapp2.RequestHandler):

    def get(self):
        form = writeForm("", "", "", "", "", "")
        content = header + form
        self.response.write(content)

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        user_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""

        if not valid_username(username):
            user_error = "That is not a valid username."

        if not valid_password(password):
            password_error  = "That was not a valid password."

        if password != verify:
            password_error = "Those passwords didn't match."

        if not valid_email(email):
            email_error = "That wasn't a valid e-mail address."

        if user_error == "" and password_error == "" and verify_error == "" and email_error == "":
            self.redirect('/welcome?username=' + username)
        else:
            form = writeForm(username, email, user_error, password_error, verify_error, email_error)
            content = header + form
            self.response.write(content)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Welcome " + self.request.get('username'))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
