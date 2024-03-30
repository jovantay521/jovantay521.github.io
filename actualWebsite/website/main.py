from flask import Flask, render_template, redirect, url_for
from backends.login import loginBp
from backends.routePlanner import routePlanBp
from backends.busExplorer import busExplorerBp

app = Flask(__name__)

#Register each page of the website as blueprint
app.register_blueprint(loginBp, url_prefix='/login')
app.register_blueprint(routePlanBp, url_prefix='/route_planner')
app.register_blueprint(busExplorerBp, url_prefix='/bus_explorer')

@app.route("/")
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)