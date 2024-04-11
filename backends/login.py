from flask import Blueprint, render_template, request, session, redirect
from database.dbAccOperation import  dbAccOp

loginBp = Blueprint("loginBp",__name__)

#renders page
@loginBp.route("/login", methods =['GET','POST'])
def login():

    return render_template('login.html')

#onclick event on form submission
@loginBp.post("/accLogin")
def accLogin_post():
    email = request.form['email']
    pwd = request.form['password']

    userdetails = [email, pwd]
    result = dbAccOp.accLogin(userdetails)
    if (result != 0):
        # print("Account " + username + "has logged in")
        session['username'] = email
        return redirect("/home")
    else:
        return redirect("/login")