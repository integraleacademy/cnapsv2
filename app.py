
from flask import Flask, render_template, request, redirect
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB_NAME = "cnaps.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
CREATE TABLE IF NOT EXISTS dossiers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    prenom TEXT,
    formation TEXT,
    session TEXT,
    lien TEXT,
    statut TEXT DEFAULT 'INCOMPLET',
    commentaire TEXT
);""")
        conn.execute("""
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    formation TEXT,
    label TEXT
);""")
init_db()

@app.route("/")
def index():
    with sqlite3.connect(DB_NAME) as conn:
        dossiers = conn.execute("SELECT * FROM dossiers").fetchall()
        sessions = conn.execute("SELECT * FROM sessions").fetchall()
    return render_template("index.html", dossiers=dossiers, sessions=sessions)

@app.route("/add", methods=["POST"])
def add():
    nom = request.form["nom"]
    prenom = request.form["prenom"]
    formation = request.form["formation"]
    session = request.form["session"]
    lien = request.form.get("lien", "")
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO dossiers (nom, prenom, formation, session, lien) VALUES (?, ?, ?, ?, ?)",
                     (nom, prenom, formation, session, lien))
    return redirect("/")

@app.route("/update_status/<int:id>", methods=["POST"])
def update_status(id):
    statut = request.form["statut"]
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE dossiers SET statut = ? WHERE id = ?", (statut, id))
    return redirect("/")

@app.route("/commentaire/<int:id>", methods=["POST"])
def commentaire(id):
    texte = request.form["commentaire"]
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE dossiers SET commentaire = ? WHERE id = ?", (texte, id))
    return redirect("/")

@app.route("/add_session", methods=["POST"])
def add_session():
    formation = request.form["formation"]
    label = request.form["label"]
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO sessions (formation, label) VALUES (?, ?)", (formation, label))
    return redirect("/")
