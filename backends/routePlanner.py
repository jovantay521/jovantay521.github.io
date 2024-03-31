from flask import Blueprint, render_template, request, redirect, url_for

routePlanBp = Blueprint("routePlanBp",__name__)

@routePlanBp.route("/route_planner", methods=['GET','POST'])
def route_planner():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('route_planner.html')

