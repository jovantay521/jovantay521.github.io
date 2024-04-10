from flask import Flask, render_template
from backends.login import loginBp
from backends.signup import signupBp
from backends.routePlanner import routePlanBp
from backends.busExplorer import busExplorerBp


app = Flask(__name__)

#Register each page of the website as blueprint
app.register_blueprint(loginBp)
app.register_blueprint(signupBp)
app.register_blueprint(routePlanBp)
app.register_blueprint(busExplorerBp)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)