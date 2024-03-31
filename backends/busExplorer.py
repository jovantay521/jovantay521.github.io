from flask import Blueprint, render_template, request, redirect, url_for

busExplorerBp = Blueprint("busExplorerBp",__name__)

@busExplorerBp.route("/bus_explorer", methods =['GET','POST'])
def bus_explorer():

    return render_template('bus_explorer.html')

