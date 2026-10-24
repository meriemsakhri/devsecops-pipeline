import os
import sqlite3

from flask import Flask, render_template_string, request
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users "
        "(id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
    )
    conn.execute("DELETE FROM users")
    conn.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("admin", generate_password_hash("S3cretPass!")),
    )
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return "Demo app. Try /login?username=admin&password=xxx"


@app.route("/login")
def login():
    username = request.args.get("username", "")
    password = request.args.get("password", "")

    conn = sqlite3.connect("users.db")
    row = conn.execute(
        "SELECT password FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()

    if row and check_password_hash(row[0], password):
        return render_template_string("Welcome {{ username }}!", username=username)
    return "Invalid credentials", 401


if __name__ == "__main__":
    init_db()
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")