from flask import Blueprint, render_template, request, session, redirect
from email_validator import validate_email, EmailNotValidError
from database.dbAccOperation import dbAccOp

signupBp = Blueprint("signupBp",__name__)

#renders page
@signupBp.route("/signup", methods =['GET','POST'])
def signup():

    return render_template('signup.html')

#onclick event on form submission
@signupBp.post("/accSignUp")
def accSignUp_post():
    username = request.form['username']
    email = request.form['email']
    pwd = request.form['password']

    userdetails = [username, email, pwd]
    result = dbAccOp.accCreate(userdetails)
    if (result != 0):
        session['username'] = username
        # print("Account " + username + " was created and added to database")
        return redirect("/home")
    else:
        return redirect("/login")