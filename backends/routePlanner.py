from flask import Blueprint, render_template, request, session

routePlanBp = Blueprint("routePlanBp",__name__)

@routePlanBp.route("/route_planner")
def route_planner():
    return render_template('route_planner.html')

