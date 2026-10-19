import sqlite3
from flask import Flask, request

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users "
        "(id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
    )
    conn.execute("DELETE FROM users")
    conn.execute("INSERT INTO users (username, password) VALUES ('admin', 'S3cretPass!')")
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
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    user = conn.execute(query).fetchone()
    conn.close()

    if user:
        return f"Welcome {username}!"
    return "Invalid credentials", 401


if __name__ == "__main__":
    init_db()
    app.run(debug=True)