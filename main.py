from flask import Flask, render_template, request, url_for, redirect
import sqlite3

#todo import flask forms stuffs

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
