from flask import Blueprint, render_template, request, redirect, url_for
from flask import session

busExplorerBp = Blueprint("busExplorerBp",__name__)

@busExplorerBp.route("/bus-explorer", methods =['GET'])
def bus_explorer():
    return render_template('bus-explorer.html')
@busExplorerBp.route("/logout")
def logout():
    session.pop('email', None)
    return redirect("/bus-explorer")

