from flask import Blueprint, render_template, request, session, redirect, flash
from database.dbAccOperation import  dbAccOp

resetBp = Blueprint("resetBp",__name__)

#renders page
@resetBp.route("/reset", methods =['GET','POST'])
def reset():
    return render_template('reset.html')

#onclick event on form submission
@resetBp.post("/accReset")
def accReset_post():
    email = request.form['email']
    pwd = request.form['password']
    cfm_pwd = request.form['confirm-password']


    if not email or not pwd or not cfm_pwd:
        flash('Please fill in all fields.')
        return redirect("/reset")

    userdetail = [email]
    result = dbAccOp.accReset(userdetail)
    if (result != 0):
        # print("Account " + username + "reset password successfully")
        session['username'] = email
        return redirect("/login")
    else:
        return redirect("/reset")