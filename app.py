
import os
import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
DB_PATH = "/mnt/data/cnaps.db"

def init_db():
    if not os.path.exists(DB_PATH):
        open(DB_PATH, "w").close()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("SELECT type FROM sessions LIMIT 1")
    except sqlite3.OperationalError:
        conn.close()
        os.remove(DB_PATH)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            nom TEXT,
            date_debut TEXT,
            date_fin TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ajouter_session", methods=["GET", "POST"])
def ajouter_session():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if request.method == "POST":
        session_type = request.form.get("type")
        nom = request.form.get("nom")
        date_debut = request.form.get("date_debut")
        date_fin = request.form.get("date_fin")

        c.execute("INSERT INTO sessions (type, nom, date_debut, date_fin) VALUES (?, ?, ?, ?)",
                  (session_type, nom, date_debut, date_fin))
        conn.commit()
        conn.close()
        return redirect("/")
    conn.close()
    return render_template("ajouter_session.html")

if __name__ == "__main__":
    app.run(debug=True)
