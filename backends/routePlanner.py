from flask import Blueprint, render_template, request, redirect, url_for

routePlanBp = Blueprint("routePlanBp",__name__)

@routePlanBp.route("/route_planner", methods=['GET','POST'])
def route_planner():

    return render_template('route_planner.html')

