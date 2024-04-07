from flask import Blueprint, render_template, request, redirect, url_for

loginBp = Blueprint("loginBp",__name__)

@loginBp.route("/login", methods =['GET','POST'])
def login():

    return render_template('login.html')

