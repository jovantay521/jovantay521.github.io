from flask import Flask, render_template, redirect, url_for, request
from backends.login import loginBp
from backends.routePlanner import routePlanBp
from backends.busExplorer import busExplorerBp

app = Flask(__name__)

#Register each page of the website as blueprint
app.register_blueprint(loginBp)
app.register_blueprint(routePlanBp)
app.register_blueprint(busExplorerBp)

# routing
@app.route('/')
@app.route('/route-planner')
def route_planner():
    return render_template('route-planner.html')

@app.route('/bus-explorer')
def bus_explorer():
    return render_template('bus-explorer.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)  