from flask import Blueprint, render_template, request, redirect, url_for

loginBp = Blueprint("loginBp",__name__)

@loginBp.route("/login", methods =['GET','POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('login.html')

