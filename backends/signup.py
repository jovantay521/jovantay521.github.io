from flask import Blueprint, render_template, request, session, redirect, flash
from email_validator import validate_email, EmailNotValidError
from requests.exceptions import HTTPError
from database.dbAccOperation import dbAccOp
import re

signupBp = Blueprint("signupBp",__name__)

#renders page
@signupBp.route("/signup", methods =['GET'])
def signup():

    return render_template('signup.html')

#onclick event on form submission
@signupBp.post("/accSignUp")
def accSignUp_post():
    username = request.form['username']
    email = request.form['email']
    pwd = request.form['password']

    
    #validation checks
    #Ensure username is more than 6 characters:
    if len(username) <=6:
        flash('Please enter an username that contains more than 6 characters.')
        return redirect("/signup")
    #Ensure password is more than 6 characters:
    elif len(pwd) <=6:
        flash('Please enter a password that contains more than 6 characters.')
        return redirect("/signup")
    
    #Ensure email is valid before account creation:
    try:
        v = validate_email(email)
        email = v["email"]
    except EmailNotValidError as e:
        flash(str(e) + " Please try again.")
        return redirect("/signup")

    userdetails = [username, email, pwd]

    try:
        result = dbAccOp.accCreate(userdetails)
        if (result != 0):
            session['email'] = email
            # print("Account " + username + " was created and added to database")
            return redirect("/route-planner")
        else:
            return redirect("/login")
        
    except HTTPError as http_err:
        if "EMAIL_EXISTS" in str(http_err):
            flash("An existing account has already been made with this username/email. Please try again.")
            return redirect("/signup")
        else:
            flash("An error has occurred. Please try again later.")
            return redirect("/login")
        