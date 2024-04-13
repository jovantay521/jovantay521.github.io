from flask import Blueprint, render_template, request, redirect, url_for

busExplorerBp = Blueprint("busExplorerBp",__name__)

@busExplorerBp.route("/bus_explorer", methods =['GET','POST'])
def bus_explorer():

    return render_template('bus_explorer.html')

@busExplorerBp.route("/userSignInCheck", methods =['GET','POST']) #check if user is logged in
def user_logged_in():
    return render_template('bus_explorer.html')