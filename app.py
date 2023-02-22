import os
import re
import io
import zlib
from werkzeug.utils import secure_filename
from flask import Response
from flask import Flask, flash, jsonify, redirect, render_template, request, session ,url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
# import face_recognition
from PIL import Image
from base64 import b64encode, b64decode
import re
import pandas as pd

import uuid
from flask_session import Session
user_app = Flask(__name__)



# Ensure templates are auto-reloaded
user_app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@user_app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter


# Configure session to use filesystem (instead of signed cookies)
user_app.config["SESSION_FILE_DIR"] = mkdtemp()
user_app.config["SESSION_PERMANENT"] = False
user_app.config["SESSION_TYPE"] = "filesystem"
Session(user_app)



@user_app.route("/")
def home():
    if "user" in session:
        df = pd.read_csv("UserDetails\\UserDetails.csv")
        data = df.to_dict('records')
        print(df)
        print(data)
        return render_template("index.html", data = data)
    else:
        return redirect('/login')

@user_app.route("/user/<string:id>")
def homeid(id):
    if "user" in session:
        df = pd.read_csv("UserDetails\\UserAttendance.csv")
        data = df[df['Id'] == int(id)]
        data = data.to_dict('records')
        data.re
        print(data)
        return render_template("userdata.html", data = data)
    else:
        return redirect('/login')

@user_app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Assign inputs to variables
        input_username = request.form.get("username")
        input_password = request.form.get("password")
        print(input_username, input_password)
        # Ensure username was submitted
        if not input_username:
            return render_template("login.html",messager = 1)


        # Ensure password was submitted
        elif not input_password:
             return render_template("login.html",messager = 2)

        # Ensure username exists and password is correct
        if input_username != 'admin' or input_password != 'admin':
            return render_template("login.html",messager = 3)

        # Remember which user has logged in
        session["user"] = 'admin'

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@user_app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")





if __name__ == '__main__':
      user_app.run()