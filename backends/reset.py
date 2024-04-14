from flask import Blueprint, render_template, request, session, redirect, flash
from database.dbAccOperation import  dbAccOp
from requests.exceptions import HTTPError
import re

resetBp = Blueprint("resetBp",__name__)

#renders page
@resetBp.route("/reset", methods =['GET','POST'])
def reset():
    return render_template('reset.html')

#onclick event on form submission
@resetBp.post("/resetPwd")
def resetPwd_post():
    email = request.form['email']
    
    result = dbAccOp.resetPwd(email)

    if(result) == 0:
        flash("Password reset email set successfully. Please relogin.")
        return redirect("/login")
    elif (result) == 1:
        flash("Invalid email. User does not exist.")
        return redirect("/reset")
    else:
        flash("Please enter an email in the field below.")
        return redirect("/reset")