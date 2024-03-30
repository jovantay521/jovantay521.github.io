from flask import Blueprint, render_template, request, session

busExplorerBp = Blueprint("busExplorerBp",__name__)

@busExplorerBp.route("/bus_explorer")
def bus_explorer():
    return render_template('bus_explorer.html')

