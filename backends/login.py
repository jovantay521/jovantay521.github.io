from flask import Blueprint, render_template, request, session

loginBp = Blueprint("loginBp",__name__)

@loginBp.route("/login", methods =['POST'])
def login():
    # from dbhandler import authLogin

    # if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    #     username = request.form['username']
    #     password = request.form['password']
    #     account = authLogin(username, password)
        
    #     if account:
    #         session['loggedin'] = True
    #         session['id'] = account['id']
    #         session['username'] = account['username']
    #         msg = 'Logged in successfully !'
    #         # return render_template('index.html', msg = msg)
    #     else:
    #         msg = 'Incorrect username / password !'
    return render_template('login.html')

