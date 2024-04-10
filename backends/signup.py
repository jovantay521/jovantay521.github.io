from flask import Blueprint, render_template, request, redirect, url_for
from email_validator import validate_email, EmailNotValidError

signupBp = Blueprint("signupBp",__name__)

@signupBp.route("/signup", methods =['GET','POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    pwd = request.form['password']

    if (len(username)>=0 | len(email)>=0 | len(pwd)>=0):
        try:
            # validate and get info
            v = validate_email(email)
            # If no error, we proceed to authenticating login
            errMsg = None

        except EmailNotValidError as e:
            # email is not valid, exception message will be displayed
            errMsg = "Invalid email. Please try again."

    return render_template('signup.html')