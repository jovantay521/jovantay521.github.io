from flask import Flask, render_template, session, request, redirect, session
from backends.login import loginBp
from backends.reset import resetBp
from backends.signup import signupBp
from backends.routePlanner import routePlanBp
from backends.busExplorer import busExplorerBp
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

#Register each page of the website as blueprint
app.register_blueprint(loginBp)
app.register_blueprint(resetBp)
app.register_blueprint(signupBp)
app.register_blueprint(routePlanBp)
app.register_blueprint(busExplorerBp)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
