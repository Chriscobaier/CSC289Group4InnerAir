from flask import Flask, render_template, request
import sqlite3

#todo import flask forms stuffs

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/login', methods=["POST"])
def login():
    return render_template("login.html")


@app.route('/register', methods=["POST"])
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run()
