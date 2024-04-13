from flask import Blueprint, render_template, request, session, redirect, flash
from database.dbAccOperation import  dbAccOp
from requests.exceptions import HTTPError
import re

loginBp = Blueprint("loginBp",__name__)

#renders page
@loginBp.route("/login", methods =['GET'])
def login():

    return render_template('login.html')

#onclick event on form submission
@loginBp.post("/accLogin")
def accLogin_post():
    email = request.form['email']
    pwd = request.form['password']

    #validation checks
    #Ensure email is valid:
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email): #checks if input contains one '@' and one '.'
        flash("Invalid email. Please enter a valid email.")
        return redirect("/login")
    #Ensure password is more than 6 characters:
    elif len(pwd) <=6:
        flash('Please enter a password that contains more than 6 characters.')
        return redirect("/login")

    userdetails = [email, pwd]

    try:
        result = dbAccOp.accLogin(userdetails)

        if (result != 0):
            # print("Account " + username + "has logged in")
            return redirect("/home")
        else:
            return redirect("/login")

    except HTTPError as http_err:
        if "INVALID_LOGIN_CREDENTIALS" in str(http_err):
            flash("Email/Password does not exist. Please try again.")
            return redirect("/login")
        else:
            flash("An error has occurred. Please try again later.")
            return redirect("/login")