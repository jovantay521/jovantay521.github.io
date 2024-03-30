from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from main import app

mysql = MySQL(app)

def authLogin(username, password):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
    account = cursor.fetchone()
    if account:
        return account
    else:
        return None